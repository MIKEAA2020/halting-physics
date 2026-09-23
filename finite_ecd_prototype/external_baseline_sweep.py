#!/usr/bin/env python3
"""Fixed-hardware external baseline sweep on identical finite instances.

Protocol of the reported experiment
-----------------------------------
- Identical instances: Boolean explicit-table instances from the controlled
  benchmark families (path-neq, binary-tree-neq, banded-chain-not-all-equal at
  width 2, grid-neq 2 x C) plus an unsatisfiable odd-ring-neq family with a
  supplied chordal-style path decomposition of width 2. All instances are
  generated as finite ECD instances and encoded to DIMACS CNF and the minimal
  CP-SAT forbidden-tuple encoding by ``baseline_encode.py``, so every solver
  sees the same finite relation data.
- Native side: the tree-decomposition dynamic program (``td-solve`` logic) is
  run with the supplied decomposition and timed; the emitted DP certificate is
  then independently re-verified and timed; for satisfiable instances a policy
  is reconstructed from the certificate and verified.
- External side: minisat, kissat, and z3 run as fresh subprocesses on the DIMACS
  file; CP-SAT runs as a fresh interpreter process on the forbidden-tuple
  encoding. Each run is bounded by a fixed wall-clock timeout, a fixed
  address-space limit, and solver-native resource flags where available.
- Cross-checking: every external SAT model is parsed, converted to a policy on
  the original instance, and verified natively; every external UNSAT answer is
  cross-checked against a natively verified DP-REFUTATION certificate. Solver
  logs are never accepted as certificates.
- Statuses: external answers are recorded as CERTIFIED-SAT-EXTERNAL or
  CERTIFIED-UNSAT-EXTERNAL only after the corresponding cross-check succeeds;
  timeouts, crashes, and unrecognised output remain INCONCLUSIVE.
- Timing: wall-clock over the whole solver process, three repetitions per
  solver and instance, median reported (min/max retained). Timings include
  process startup. CP-SAT timings additionally include interpreter startup and
  model construction.

Output: reports/external_baseline_sweep.json plus per-instance artifacts in
examples/ with prefix ``xbase_``.
"""
from __future__ import annotations
import argparse, itertools, json, os, platform, resource, shutil, subprocess, sys, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from finite_ecd import (
    Instance, verify_policy, verify_dp_certificate, td_dynamic_program,
    assignment_key,
)
from benchmark_gen import path_instance, tree_instance, band_instance, grid_instance
from baseline_encode import to_dimacs, to_cpsat_json, to_milp_lp

TIMEOUT_SECONDS = 60.0
MEMORY_LIMIT_BYTES = 3 * 1024 ** 3
REPETITIONS = 3
tempfile_iterator = itertools.count()


# ---------------------------------------------------------------------------
# Instance families
# ---------------------------------------------------------------------------

def ring_instance(n: int):
    """Odd ring of disequality factors; unsatisfiable when n is odd.

    Supplied decomposition: chordal-style path decomposition with bags
    [x0, xi, xi+1] for i = 1..n-2, which has width 2 for n >= 3.
    """
    variables = [f"x{i}" for i in range(n)]
    neq = [[0, 1], [1, 0]]
    factors = [
        {"name": f"neq{i}_{(i + 1) % n}", "scope": [f"x{i}", f"x{(i + 1) % n}"],
         "relation": [list(r) for r in neq]}
        for i in range(n)
    ]
    bags = {f"b{i}": [variables[0], variables[i], variables[i + 1]] for i in range(1, n - 1)}
    edges = [[f"b{i}", f"b{i + 1}"] for i in range(1, n - 2)]
    f2b = {}
    for f in factors:
        a, b = f["scope"]
        i, j = int(a[1:]), int(b[1:])
        if i == 0 and j == n - 1 or i == n - 1 and j == 0:
            f2b[f["name"]] = f"b{n - 2}"
        elif min(i, j) == 0:
            f2b[f["name"]] = f"b{max(i, j)}"
        else:
            f2b[f["name"]] = f"b{min(i, j)}"
    inst = {
        "variables": variables,
        "domains": {x: [0, 1] for x in variables},
        "value_costs": {x: {"0": 0, "1": 1} for x in variables},
        "factors": factors,
        "metadata": {"family": "odd-ring-neq", "n": n, "expected": "UNSAT" if n % 2 == 1 else "SAT",
                     "supplied_decomposition_width": 2},
    }
    decomp = {"type": "TREE-DECOMP", "root": "b1", "bags": bags, "edges": edges,
              "factor_to_bag": f2b, "metadata": {"width": 2, "family": "odd-ring-neq"}}
    return inst, decomp


def build_cases():
    cases = []
    for n in [8, 32, 128, 512, 2048]:
        cases.append({"family": "path-neq", "n": n, "gen": lambda n=n: path_instance(n)})
    for depth in [2, 4, 6, 8, 9]:
        cases.append({"family": "binary-tree-neq", "n": 2 ** (depth + 1) - 1,
                      "gen": lambda d=depth: tree_instance(d)})
    for n in [8, 32, 128, 512, 2048]:
        cases.append({"family": "banded-chain-w2", "n": n,
                      "gen": lambda n=n: band_instance(n, 2)})
    for cols in [4, 16, 64, 256]:
        cases.append({"family": "grid-neq-2xC", "n": 2 * cols,
                      "gen": lambda c=cols: grid_instance(2, c)})
    for n in [5, 17, 65, 257, 1025]:
        cases.append({"family": "odd-ring-neq", "n": n, "gen": lambda n=n: ring_instance(n)})
    return cases


# ---------------------------------------------------------------------------
# Native pipeline
# ---------------------------------------------------------------------------

def reconstruct_policy(cert):
    """Reconstruct a global policy from a DP-OPTIMUM certificate."""
    bags = cert["tree_decomp"]["bags"]
    root = cert["root"]
    edges = cert["tree_decomp"]["edges"]
    adj = {b: [] for b in bags}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    assignment = {}
    root_vals = cert["root_assignment"]
    if root_vals is None:
        return None
    for x, v in zip(bags[root], root_vals):
        assignment[x] = v
    queue = [root]
    visited = {root}
    argmins = cert["argmins"]
    while queue:
        b = queue.pop(0)
        key = assignment_key([assignment[x] for x in bags[b]])
        for ch in adj[b]:
            if ch in visited:
                continue
            visited.add(ch)
            ch_vals = argmins.get(b, {}).get(key, {}).get(ch)
            if ch_vals is None:
                return None
            for x, v in zip(bags[ch], ch_vals):
                assignment[x] = v
            queue.append(ch)
    return assignment


def native_run(inst_raw, decomp):
    inst = Instance.from_json(inst_raw)
    t0 = time.perf_counter()
    cert = td_dynamic_program(inst, inst_raw, decomp)
    t1 = time.perf_counter()
    ok, errors = verify_dp_certificate(inst, inst_raw, cert)
    t2 = time.perf_counter()
    out = {
        "dp_status": cert["status"],
        "certificate_type": cert["type"],
        "dp_seconds": round(t1 - t0, 6),
        "verify_seconds": round(t2 - t1, 6),
        "certificate_verified": bool(ok),
        "certificate_errors": errors,
    }
    if cert["type"] == "DP-OPTIMUM":
        policy = reconstruct_policy(cert)
        if policy is None:
            out["policy_verified"] = False
            out["policy_errors"] = ["could not reconstruct policy from certificate"]
        else:
            pok, perr = verify_policy(inst, policy)
            out["policy_verified"] = bool(pok)
            out["policy_errors"] = perr
            out["policy_certificate"] = {"type": "POLICY", "assignment": policy}
    return out, cert


# ---------------------------------------------------------------------------
# External solver execution
# ---------------------------------------------------------------------------

def _apply_limits():
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES))


def _safe_kill(proc):
    try:
        proc.kill()
    except Exception:
        pass


_RUN_TMP = ROOT / "reports" / "_run_tmp"


def run_with_limits(cmd, timeout):
    """Run a command under the fixed limits.

    Captures stdout/stderr to files and reaps the child with os.wait4 so that
    the peak resident set size is measured per child process. Returns
    (returncode, stdout, stderr, elapsed_seconds, peak_rss_kib).
    """
    _RUN_TMP.mkdir(parents=True, exist_ok=True)
    out_path = _RUN_TMP / f"run_{next(tempfile_iterator)}.out"
    err_path = _RUN_TMP / f"run_{next(tempfile_iterator)}.err"
    t0 = time.perf_counter()
    with open(out_path, "w") as so, open(err_path, "w") as se:
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=so, stderr=se,
                                preexec_fn=_apply_limits)
        timer = threading.Timer(timeout, _safe_kill, args=(proc,))
        timer.start()
        try:
            _, status, ru = os.wait4(proc.pid, 0)
        finally:
            timer.cancel()
    elapsed = time.perf_counter() - t0
    try:
        rc = os.waitstatus_to_exitcode(status)
    except ValueError:
        rc = None
    out = out_path.read_text()
    err = err_path.read_text()
    return rc, out, err, elapsed, ru.ru_maxrss


def parse_sat_model(text):
    """Parse 'v' lines from SAT solver output into {var_index: bool}."""
    model = {}
    for line in text.splitlines():
        if line.startswith("v "):
            for tok in line[2:].split():
                if tok == "0":
                    continue
                try:
                    lit = int(tok)
                except ValueError:
                    return None
                model[abs(lit)] = lit > 0
    return model or None


def classify(status_token, exit_code):
    tok = (status_token or "").strip().upper()
    # NOTE: "UNSATISFIABLE" contains "SATISFIABLE" as a substring, so exact
    # forms are checked first.
    if "UNSATISFIABLE" in tok or tok == "UNSAT":
        return "UNSAT"
    if "SATISFIABLE" in tok or tok == "SAT":
        return "SAT"
    if "INDET" in tok or "UNKNOWN" in tok:
        return "INDET"
    return None


def model_to_policy(model, variables):
    if model is None:
        return None
    assignment = {}
    for i, x in enumerate(variables):
        if (i + 1) not in model:
            return None
        assignment[x] = 1 if model[i + 1] else 0
    return assignment


def run_minisat(exe, cnf, resultfile):
    resultfile.unlink(missing_ok=True)
    cmd = [exe, "-mem-lim=3072", "-cpu-lim=60", str(cnf), str(resultfile)]
    rc, out, err, elapsed, rss = run_with_limits(cmd, TIMEOUT_SECONDS)
    token = ""
    restext = ""
    if resultfile.exists():
        restext = resultfile.read_text().strip()
        token = restext.splitlines()[0] if restext else ""
    cls = classify(token, rc) or classify(out, rc)
    model = None
    if cls == "SAT" and restext:
        lits = restext.split()
        model = {}
        try:
            for tok in lits[1:]:
                if tok == "0":
                    continue
                model[abs(int(tok))] = int(tok) > 0
        except ValueError:
            model = None
    return {"solver": "minisat", "classification": cls, "returncode": rc,
            "seconds": elapsed, "peak_rss_kib": rss, "model": model,
            "stdout_tail": out[-400:]}


def run_kissat(exe, cnf):
    cmd = [exe, "--time=60", str(cnf)]
    rc, out, err, elapsed, rss = run_with_limits(cmd, TIMEOUT_SECONDS)
    token = ""
    for line in out.splitlines():
        if line.startswith("s "):
            token = line[2:]
            break
    cls = classify(token, rc) or classify(out, rc)
    model = parse_sat_model(out) if cls == "SAT" else None
    return {"solver": "kissat", "classification": cls, "returncode": rc,
            "seconds": elapsed, "peak_rss_kib": rss, "model": model,
            "stdout_tail": out[-400:]}


def run_z3(exe, cnf):
    cmd = [exe, "-T:60", str(cnf)]
    rc, out, err, elapsed, rss = run_with_limits(cmd, TIMEOUT_SECONDS)
    token = ""
    for line in out.splitlines():
        if line.startswith("s "):
            token = line[2:]
            break
    cls = classify(token, rc) or classify(out, rc)
    model = parse_sat_model(out) if cls == "SAT" else None
    return {"solver": "z3", "classification": cls, "returncode": rc,
            "seconds": elapsed, "peak_rss_kib": rss, "model": model,
            "stdout_tail": out[-400:]}


def run_cpsat(python, encoding):
    cmd = [str(python), str(ROOT / "cpsat_runner.py"), str(encoding),
           "--time-limit", str(TIMEOUT_SECONDS), "--seed", "1"]
    rc, out, err, elapsed, rss = run_with_limits(cmd, TIMEOUT_SECONDS + 30.0)
    try:
        payload = json.loads(out)
    except Exception:
        payload = None
    if payload is None:
        return {"solver": "cpsat", "classification": None, "returncode": rc,
                "seconds": elapsed, "peak_rss_kib": rss, "model": None,
                "stderr_tail": err[-400:]}
    cls = {"CERTIFIED-SAT-EXTERNAL": "SAT",
           "CERTIFIED-UNSAT-EXTERNAL": "UNSAT"}.get(payload.get("status"))
    model = payload.get("model")
    return {"solver": "cpsat", "classification": cls, "returncode": rc,
            "seconds": elapsed, "peak_rss_kib": rss, "model": model,
            "build_seconds": payload.get("build_seconds"),
            "solve_seconds": payload.get("solve_seconds"),
            "inner_peak_rss_kib": payload.get("peak_rss_kib")}


def run_highs(python, lp_file):
    cmd = [str(python), str(ROOT / "highs_runner.py"), str(lp_file),
           "--time-limit", str(TIMEOUT_SECONDS)]
    rc, out, err, elapsed, rss = run_with_limits(cmd, TIMEOUT_SECONDS + 30.0)
    try:
        payload = json.loads(out)
    except Exception:
        payload = None
    if payload is None:
        return {"solver": "highs", "classification": None, "returncode": rc,
                "seconds": elapsed, "peak_rss_kib": rss, "model": None,
                "stderr_tail": err[-400:]}
    cls = {"CERTIFIED-SAT-EXTERNAL": "SAT",
           "CERTIFIED-UNSAT-EXTERNAL": "UNSAT"}.get(payload.get("status"))
    model = payload.get("model")
    return {"solver": "highs", "classification": cls, "returncode": rc,
            "seconds": elapsed, "peak_rss_kib": rss, "model": model,
            "build_seconds": payload.get("build_seconds"),
            "solve_seconds": payload.get("solve_seconds"),
            "inner_peak_rss_kib": payload.get("peak_rss_kib")}


# ---------------------------------------------------------------------------
# Experiment driver
# ---------------------------------------------------------------------------

def hardware_info():
    cpu = ""
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    except Exception:
        cpu = platform.processor() or "unknown"
    mem = ""
    try:
        mem = subprocess.run(["free", "-h"], capture_output=True, text=True).stdout
        mem = [l for l in mem.splitlines() if l.startswith("Mem:")][0].split()[1]
    except Exception:
        pass
    return {
        "cpu": cpu,
        "cores": os.cpu_count(),
        "ram_total": mem,
        "os": " ".join(platform.libc_ver()) or platform.system(),
        "kernel": platform.release(),
        "machine_python": sys.version.split()[0],
        "note": "wall-clock timings are whole-process and include solver startup; "
                "machine is a shared two-core virtual machine",
    }


def median(xs):
    s = sorted(xs)
    return s[len(s) // 2]


def _solver_version(exe):
    """Best-effort version string for a solver executable."""
    for flag in ("--version", "-version"):
        try:
            p = subprocess.run([exe, flag], capture_output=True, text=True,
                               timeout=10)
            line = (p.stdout or p.stderr).strip().splitlines()
            if line:
                return line[0][:120]
        except Exception:
            continue
    return "unknown version"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/external_baseline_sweep.json")
    ap.add_argument("--minisat", default=os.environ.get("EXTERNAL_ECD_MINISAT")
                    or shutil.which("minisat"))
    ap.add_argument("--kissat", default=os.environ.get("EXTERNAL_ECD_KISSAT")
                    or shutil.which("kissat"))
    ap.add_argument("--z3", default=os.environ.get("EXTERNAL_ECD_Z3")
                    or shutil.which("z3"))
    ap.add_argument("--cpsat-python",
                    default=os.environ.get("EXTERNAL_ECD_CPSAT_PYTHON"),
                    help="interpreter with ortools installed; when omitted, the "
                         "current interpreter is used if it can import ortools")
    ap.add_argument("--highs-python",
                    default=os.environ.get("EXTERNAL_ECD_HIGHS_PYTHON"),
                    help="interpreter with highspy installed; when omitted, the "
                         "current interpreter is used if it can import highspy")
    ap.add_argument("--repetitions", type=int, default=REPETITIONS)
    args = ap.parse_args()

    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "examples").mkdir(exist_ok=True)

    cpsat_python = args.cpsat_python
    if cpsat_python is None:
        try:
            import importlib.metadata as md
            md.version("ortools")
            cpsat_python = sys.executable
        except Exception:
            cpsat_python = None

    highs_python = args.highs_python
    if highs_python is None:
        try:
            import importlib.metadata as md
            md.version("highspy")
            highs_python = sys.executable
        except Exception:
            highs_python = None

    solvers = {}
    if args.minisat:
        solvers["minisat"] = {"exe": args.minisat,
                              "version": "minisat 2.2 series (arminbiere mirror "
                                         "commit 16982a5, gcc 14.2, -O3)"}
    if args.kissat:
        solvers["kissat"] = {"exe": args.kissat,
                             "version": "kissat 4.0.4 (commit 8af8e56, "
                                        "gcc 14.2, -O3)"}
    if args.z3:
        solvers["z3"] = {"exe": args.z3, "version": _solver_version(args.z3)}
    if cpsat_python:
        try:
            import importlib.metadata as md
            ver = md.version("ortools") if cpsat_python == sys.executable else None
        except Exception:
            ver = None
        if ver is None:
            p = subprocess.run([cpsat_python, "-c",
                                "import importlib.metadata as m; "
                                "print(m.version('ortools'))"],
                               capture_output=True, text=True, timeout=60)
            ver = p.stdout.strip() or "unknown"
        solvers["cpsat"] = {"exe": cpsat_python,
                            "version": f"OR-Tools CP-SAT {ver}"}
    if highs_python:
        try:
            import importlib.metadata as md
            ver = md.version("highspy") if highs_python == sys.executable else None
        except Exception:
            ver = None
        if ver is None:
            p = subprocess.run([highs_python, "-c",
                                "import importlib.metadata as m; "
                                "print(m.version('highspy'))"],
                               capture_output=True, text=True, timeout=60)
            ver = p.stdout.strip() or "unknown"
        solvers["highs"] = {"exe": highs_python,
                            "version": f"HiGHS MILP {ver}"}

    if not solvers:
        out = {
            "status": "INCONCLUSIVE",
            "reason": "no supported external solver installed",
            "protocol": {
                "timeout_seconds": TIMEOUT_SECONDS,
                "memory_limit_bytes": MEMORY_LIMIT_BYTES,
                "hardware": hardware_info(),
            },
        }
        out_path = ROOT / args.out
        out_path.write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2))
        return

    protocol = {
        "timeout_seconds": TIMEOUT_SECONDS,
        "memory_limit_bytes": MEMORY_LIMIT_BYTES,
        "memory_limit_note": "address space cap applied to every external solver process",
        "repetitions": args.repetitions,
        "timing": "wall clock over the whole process; median of repetitions reported",
        "determinism": "single-threaded configurations; CP-SAT num_workers=1 with "
                       "random_seed=1; minisat and kissat default deterministic "
                       "configurations; no randomization flags otherwise",
        "hardware": hardware_info(),
        "solvers": {k: v["version"] for k, v in solvers.items()},
        "cross_check_discipline": "external SAT models are verified natively as "
                                  "policies on the original instance; external UNSAT "
                                  "answers are cross-checked against verified "
                                  "DP-REFUTATION certificates; solver logs are not "
                                  "certificates",
    }

    cases_out = []
    for idx, case in enumerate(build_cases()):
        prefix = ROOT / "examples" / f"xbase_{case['family']}_n{case['n']}"
        inst_raw, decomp = case["gen"]()
        variables = inst_raw["variables"]
        inst_path = Path(str(prefix) + "_instance.json")
        dec_path = Path(str(prefix) + "_tree_decomp.json")
        cnf_path = Path(str(prefix) + ".cnf")
        cpsat_path = Path(str(prefix) + "_cpsat.json")
        lp_path = Path(str(prefix) + ".lp")
        dp_path = Path(str(prefix) + "_dp_certificate.json")
        inst_path.write_text(json.dumps(inst_raw, indent=2))
        dec_path.write_text(json.dumps(decomp, indent=2))
        cnf_path.write_text(to_dimacs(inst_raw))
        cpsat_path.write_text(json.dumps(to_cpsat_json(inst_raw), indent=2))
        lp_path.write_text(to_milp_lp(inst_raw))

        t0 = time.perf_counter()
        cnf_text = to_dimacs(inst_raw)
        encode_seconds = time.perf_counter() - t0
        n_clauses = cnf_text.count(" 0\n")
        expected = inst_raw.get("metadata", {}).get("expected",
                     "UNSAT" if case["family"] == "odd-ring-neq" else "SAT")

        native, cert = native_run(inst_raw, decomp)
        dp_path.write_text(json.dumps(cert, indent=2))
        if native.get("policy_certificate"):
            Path(str(prefix) + "_policy_certificate.json").write_text(
                json.dumps(native["policy_certificate"], indent=2))

        entry = {
            "family": case["family"], "n": case["n"],
            "instance": str(inst_path.relative_to(ROOT)),
            "variables": len(variables),
            "factors": len(inst_raw["factors"]),
            "cnf_clauses": n_clauses,
            "encode_seconds": round(encode_seconds, 6),
            "expected": expected,
            "native": {k: v for k, v in native.items() if k != "policy_certificate"},
            "external": [],
        }

        inst_obj = Instance.from_json(inst_raw)
        for name, cfg in solvers.items():
            reps = []
            for r in range(args.repetitions):
                if name == "minisat":
                    resfile = Path(str(prefix) + f"_minisat_res_{r}")
                    raw = run_minisat(cfg["exe"], cnf_path, resfile)
                elif name == "kissat":
                    raw = run_kissat(cfg["exe"], cnf_path)
                elif name == "z3":
                    raw = run_z3(cfg["exe"], cnf_path)
                elif name == "highs":
                    raw = run_highs(cfg["exe"], lp_path)
                else:
                    raw = run_cpsat(cfg["exe"], cpsat_path)
                reps.append(raw)
            seconds = [r["seconds"] for r in reps]
            rep = reps[0]
            cls = rep["classification"]
            cross = {"status": "INCONCLUSIVE",
                     "reason": "external run did not produce a recognised status"}
            if cls == "SAT":
                if name in ("cpsat", "highs"):
                    # The CP-SAT and HiGHS runners report models directly as
                    # variable-name -> value policy maps.
                    policy = rep.get("model")
                    if policy is not None:
                        policy = {k: int(v) for k, v in policy.items()}
                else:
                    policy = model_to_policy(rep.get("model"), variables)
                if policy is None:
                    cross = {"status": "INCONCLUSIVE",
                             "reason": "external model incomplete or unparsable"}
                else:
                    ok, errors = verify_policy(inst_obj, policy)
                    if ok:
                        cross = {"status": "VERIFIED-SAT",
                                 "external_status": "CERTIFIED-SAT-EXTERNAL",
                                 "model_policy_verified": True}
                    else:
                        cross = {"status": "REJECTED", "errors": errors}
            elif cls == "UNSAT":
                if cert["type"] == "DP-REFUTATION" and native["certificate_verified"]:
                    cross = {"status": "VERIFIED-UNSAT",
                             "external_status": "CERTIFIED-UNSAT-EXTERNAL",
                             "native_certificate": "DP-REFUTATION verified"}
                else:
                    cross = {"status": "INCONCLUSIVE",
                             "reason": "no verified native DP-REFUTATION for cross-check"}
            ext = {
                "solver": name,
                "classification": cls,
                "seconds_median": round(median(seconds), 6),
                "seconds_min": round(min(seconds), 6),
                "seconds_max": round(max(seconds), 6),
                "peak_rss_kib": max(r.get("peak_rss_kib") or 0 for r in reps),
                "returncode": rep.get("returncode"),
                "cross_check": cross,
            }
            for extra in ("build_seconds", "solve_seconds", "inner_peak_rss_kib"):
                if rep.get(extra) is not None:
                    ext[extra] = rep[extra]
            entry["external"].append(ext)
            print(f"  {case['family']} n={case['n']} {name}: {cls} "
                  f"{ext['seconds_median']}s cross={cross['status']}", flush=True)
        cases_out.append(entry)

    summary = {
        "instances": len(cases_out),
        "native_certificates_verified": sum(
            1 for c in cases_out if c["native"]["certificate_verified"]),
        "native_policies_verified": sum(
            1 for c in cases_out if c["native"].get("policy_verified")),
        "external_runs": sum(len(c["external"]) for c in cases_out),
        "external_sat_cross_checked": sum(
            1 for c in cases_out for e in c["external"]
            if e["cross_check"]["status"] == "VERIFIED-SAT"),
        "external_unsat_cross_checked": sum(
            1 for c in cases_out for e in c["external"]
            if e["cross_check"]["status"] == "VERIFIED-UNSAT"),
        "external_inconclusive": sum(
            1 for c in cases_out for e in c["external"]
            if e["cross_check"]["status"] == "INCONCLUSIVE"),
        "external_rejected": sum(
            1 for c in cases_out for e in c["external"]
            if e["cross_check"]["status"] == "REJECTED"),
        "status_agreement_with_native": sum(
            1 for c in cases_out for e in c["external"]
            if e["classification"] is not None
            and e["classification"] == c["native"]["dp_status"].replace("CERTIFIED-", "").replace("OPT", "SAT")
            and e["cross_check"]["status"] in ("VERIFIED-SAT", "VERIFIED-UNSAT")),
    }
    out = {"status": "COMPLETE", "protocol": protocol, "cases": cases_out,
           "summary": summary}
    out_path = ROOT / args.out
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
