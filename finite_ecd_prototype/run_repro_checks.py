#!/usr/bin/env python3
"""Run the current finite ECD prototype reproducibility checks."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable


def run_tool(tool: str, args):
    proc = subprocess.run([PYTHON, str(ROOT / tool), *args], cwd=ROOT, text=True, capture_output=True)
    try:
        payload = json.loads(proc.stdout)
    except Exception:
        payload = {"raw_stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}
    return payload


def run(args):
    return run_tool("finite_ecd.py", args)


def run_fe(args):
    return run_tool("affine_fe.py", args)


def run_text(tool: str, args):
    proc = subprocess.run([PYTHON, str(ROOT / tool), *args], cwd=ROOT, text=True, capture_output=True)
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def main():
    gen = subprocess.run([PYTHON, str(ROOT / "two_spring_generator.py")], cwd=ROOT, text=True, capture_output=True)

    same = run(["solve", "examples/generated_two_spring_same.json"])
    split = run(["solve", "examples/generated_two_spring_split.json"])
    fibre = run(["fibre-conflict", "examples/two_spring_fibres.json", "same"])
    fibre_cert = ROOT / "examples/two_spring_fibre_conflict_certificate.json"
    fibre_cert.write_text(json.dumps(fibre, indent=2))
    fibre_verify = run(["verify-fibre", "examples/two_spring_fibres.json", str(fibre_cert)])

    bad_fibre = json.loads(fibre_cert.read_text())
    bad_fibre["witnesses"][0]["action"] = [0, 1]
    bad_fibre_cert = ROOT / "examples/bad_fibre_conflict_certificate.json"
    bad_fibre_cert.write_text(json.dumps(bad_fibre, indent=2))
    bad_fibre_verify = run(["verify-fibre", "examples/two_spring_fibres.json", str(bad_fibre_cert)])

    sensor = run(["sensor-repair", "examples/two_spring_sensors.json"])
    sensor_cert = ROOT / "examples/two_spring_sensor_repair_certificate.json"
    sensor_cert.write_text(json.dumps(sensor, indent=2))
    sensor_verify = run(["verify-sensor-repair", "examples/two_spring_sensors.json", str(sensor_cert)])

    bad_sensor = dict(sensor)
    bad_sensor["selected"] = ["constant"]
    bad_sensor_cert = ROOT / "examples/bad_sensor_repair_certificate.json"
    bad_sensor_cert.write_text(json.dumps(bad_sensor, indent=2))
    bad_sensor_verify = run(["verify-sensor-repair", "examples/two_spring_sensors.json", str(bad_sensor_cert)])

    tree_decomp = run(["tree-decomp", "examples/tiny_cost_sat.json"])
    tree_decomp_cert = ROOT / "examples/tiny_cost_tree_decomp.json"
    tree_decomp_cert.write_text(json.dumps(tree_decomp, indent=2))
    tree_decomp_verify = run(["verify-tree-decomp", "examples/tiny_cost_sat.json", str(tree_decomp_cert)])
    dp_opt = run(["td-solve", "examples/tiny_cost_sat.json", "--decomp", str(tree_decomp_cert)])
    dp_opt_cert = ROOT / "examples/tiny_cost_dp_certificate.json"
    dp_opt_cert.write_text(json.dumps(dp_opt, indent=2))
    dp_opt_verify = run(["verify-dp", "examples/tiny_cost_sat.json", str(dp_opt_cert)])
    dp_ref = run(["td-solve", "examples/two_spring_fe_instance.json"])
    dp_ref_cert = ROOT / "examples/two_spring_dp_refutation_certificate.json"
    dp_ref_cert.write_text(json.dumps(dp_ref, indent=2))
    dp_ref_verify = run(["verify-dp", "examples/two_spring_fe_instance.json", str(dp_ref_cert)])
    bad_dp = json.loads(dp_opt_cert.read_text())
    bag = next(iter(bad_dp["messages"]))
    for row in bad_dp["messages"][bag]["table"]:
        if row["cost"] is not None:
            row["cost"] += 99
            break
    bad_dp_cert = ROOT / "examples/bad_tiny_cost_dp_certificate.json"
    bad_dp_cert.write_text(json.dumps(bad_dp, indent=2))
    bad_dp_verify = run(["verify-dp", "examples/tiny_cost_sat.json", str(bad_dp_cert)])

    fe_rows = run_fe(["generate", "examples/two_spring_affine_model.json"])
    fe_cert = ROOT / "examples/two_spring_fe_rows.json"
    fe_cert.write_text(json.dumps(fe_rows, indent=2))
    (ROOT / "examples/two_spring_fe_instance.json").write_text(json.dumps(fe_rows["instance"], indent=2))
    fe_verify = run_fe(["verify", "examples/two_spring_affine_model.json", str(fe_cert)])
    bad_fe = json.loads(fe_cert.read_text())
    bad_fe["rows"][0]["classification"] = "SAFE" if bad_fe["rows"][0]["classification"] != "SAFE" else "UNSAFE"
    bad_fe_cert = ROOT / "examples/bad_two_spring_fe_rows.json"
    bad_fe_cert.write_text(json.dumps(bad_fe, indent=2))
    bad_fe_verify = run_fe(["verify", "examples/two_spring_affine_model.json", str(bad_fe_cert)])

    spars = run_fe(["sparsify", "examples/two_spring_affine_model.json", "examples/two_spring_retained_a1.json"])
    spars_cert = ROOT / "examples/two_spring_sparsification_certificate.json"
    spars_cert.write_text(json.dumps(spars, indent=2))
    spars_verify = run_fe(["verify-sparsify", "examples/two_spring_affine_model.json", str(spars_cert)])
    bad_spars = json.loads(spars_cert.read_text())
    bad_spars["rows"][0]["inner"] = not bad_spars["rows"][0]["inner"]
    bad_spars_cert = ROOT / "examples/bad_two_spring_sparsification_certificate.json"
    bad_spars_cert.write_text(json.dumps(bad_spars, indent=2))
    bad_spars_verify = run_fe(["verify-sparsify", "examples/two_spring_affine_model.json", str(bad_spars_cert)])

    path_td_verify = run(["verify-tree-decomp", "examples/path3_sat.json", "examples/path3_tree_decomp.json"])
    path_dp = run(["td-solve", "examples/path3_sat.json", "--decomp", "examples/path3_tree_decomp.json"])
    (ROOT / "examples/path3_dp_optimum_certificate.json").write_text(json.dumps(path_dp, indent=2))
    path_dp_verify = run(["verify-dp", "examples/path3_sat.json", "examples/path3_dp_optimum_certificate.json"])
    path_ref = run(["td-solve", "examples/path3_unsat.json", "--decomp", "examples/path3_unsat_tree_decomp.json"])
    (ROOT / "examples/path3_dp_refutation_certificate.json").write_text(json.dumps(path_ref, indent=2))
    path_ref_verify = run(["verify-dp", "examples/path3_unsat.json", "examples/path3_dp_refutation_certificate.json"])

    dimacs = run_text("baseline_encode.py", ["dimacs", "examples/path3_sat.json"])
    (ROOT / "examples/path3_sat.cnf").write_text(dimacs["stdout"])
    milp = run_text("baseline_encode.py", ["milp-lp", "examples/path3_sat.json"])
    (ROOT / "examples/path3_sat.lp").write_text(milp["stdout"])
    cpsat = run_text("baseline_encode.py", ["cpsat-json", "examples/path3_sat.json"])
    (ROOT / "examples/path3_sat_cpsat.json").write_text(cpsat["stdout"])
    missing_solver = run_text("external_solver_adapter.py", ["--name", "missing-test", "--timeout", "1", "--", "definitely_missing_solver", "examples/path3_sat.cnf"])
    (ROOT / "examples/external_missing_solver_result.json").write_text(missing_solver["stdout"])

    gen_path = run_text("benchmark_gen.py", ["path", "6", "examples/generated_path6"])
    gen_path_td_verify = run(["verify-tree-decomp", "examples/generated_path6_instance.json", "examples/generated_path6_tree_decomp.json"])
    gen_path_dp = run(["td-solve", "examples/generated_path6_instance.json", "--decomp", "examples/generated_path6_tree_decomp.json"])
    (ROOT / "examples/generated_path6_dp_certificate.json").write_text(json.dumps(gen_path_dp, indent=2))
    gen_path_dp_verify = run(["verify-dp", "examples/generated_path6_instance.json", "examples/generated_path6_dp_certificate.json"])
    gen_tree = run_text("benchmark_gen.py", ["binary-tree", "2", "examples/generated_btree_depth2"])
    gen_tree_td_verify = run(["verify-tree-decomp", "examples/generated_btree_depth2_instance.json", "examples/generated_btree_depth2_tree_decomp.json"])
    gen_tree_dp = run(["td-solve", "examples/generated_btree_depth2_instance.json", "--decomp", "examples/generated_btree_depth2_tree_decomp.json"])
    (ROOT / "examples/generated_btree_depth2_dp_certificate.json").write_text(json.dumps(gen_tree_dp, indent=2))
    gen_tree_dp_verify = run(["verify-dp", "examples/generated_btree_depth2_instance.json", "examples/generated_btree_depth2_dp_certificate.json"])

    fine_spars = run_fe(["sparsify", "examples/two_spring_affine_model.json", "examples/two_spring_retained_a1a2.json"])
    fine_spars_cert = ROOT / "examples/two_spring_sparsification_fine_certificate.json"
    fine_spars_cert.write_text(json.dumps(fine_spars, indent=2))
    ladder_verify = run_fe(["verify-sparsify-ladder", "examples/two_spring_affine_model.json", str(spars_cert), str(fine_spars_cert)])

    frame_rows = run_fe(["generate", "examples/four_actuator_frame_affine_model.json"])
    frame_cert = ROOT / "examples/four_actuator_frame_fe_rows.json"
    frame_cert.write_text(json.dumps(frame_rows, indent=2))
    (ROOT / "examples/four_actuator_frame_fe_instance.json").write_text(json.dumps(frame_rows["instance"], indent=2))
    frame_verify = run_fe(["verify", "examples/four_actuator_frame_affine_model.json", str(frame_cert)])
    frame_dp = run(["td-solve", "examples/four_actuator_frame_fe_instance.json"])
    (ROOT / "examples/four_actuator_frame_dp_certificate.json").write_text(json.dumps(frame_dp, indent=2))
    frame_dp_verify = run(["verify-dp", "examples/four_actuator_frame_fe_instance.json", "examples/four_actuator_frame_dp_certificate.json"])

    cross_sat = run_text("cross_check_external.py", ["examples/fake_external_sat.json", "examples/path3_sat.json", "--policy", "examples/path3_policy_certificate.json"])
    (ROOT / "examples/cross_checked_external_sat.json").write_text(cross_sat["stdout"])
    cross_unsat = run_text("cross_check_external.py", ["examples/fake_external_unsat.json", "examples/path3_unsat.json", "--refutation", "examples/path3_dp_refutation_certificate.json"])
    (ROOT / "examples/cross_checked_external_unsat.json").write_text(cross_unsat["stdout"])
    cross_sat_nocert = run_text("cross_check_external.py", ["examples/fake_external_sat.json", "examples/path3_sat.json"])
    (ROOT / "examples/cross_checked_external_sat_no_cert.json").write_text(cross_sat_nocert["stdout"])

    band_gen = run_text("benchmark_gen.py", ["band", "7", "examples/generated_band7_w2", "--width", "2"])
    band_td = run(["verify-tree-decomp", "examples/generated_band7_w2_instance.json", "examples/generated_band7_w2_tree_decomp.json"])
    band_dp = run(["td-solve", "examples/generated_band7_w2_instance.json", "--decomp", "examples/generated_band7_w2_tree_decomp.json"])
    (ROOT / "examples/generated_band7_w2_dp_certificate.json").write_text(json.dumps(band_dp, indent=2))
    band_dp_verify = run(["verify-dp", "examples/generated_band7_w2_instance.json", "examples/generated_band7_w2_dp_certificate.json"])
    grid_gen = run_text("benchmark_gen.py", ["grid", "2", "examples/generated_grid2x4", "--cols", "4"])
    grid_td = run(["verify-tree-decomp", "examples/generated_grid2x4_instance.json", "examples/generated_grid2x4_tree_decomp.json"])
    grid_dp = run(["td-solve", "examples/generated_grid2x4_instance.json", "--decomp", "examples/generated_grid2x4_tree_decomp.json"])
    (ROOT / "examples/generated_grid2x4_dp_certificate.json").write_text(json.dumps(grid_dp, indent=2))
    grid_dp_verify = run(["verify-dp", "examples/generated_grid2x4_instance.json", "examples/generated_grid2x4_dp_certificate.json"])
    grid_summary = run_text("report_summary.py", ["examples/generated_grid2x4_instance.json", "--decomp", "examples/generated_grid2x4_tree_decomp.json", "--certificate", "examples/generated_grid2x4_dp_certificate.json"])
    (ROOT / "examples/generated_grid2x4_summary.json").write_text(grid_summary["stdout"])

    # mechanics smoke checks (phase 4 families, small representatives)
    import mechanics_fe
    import mechanics_gen as mgen
    from finite_ecd import Instance as MInstance
    from finite_ecd import validate_tree_decomp as mvalidate_td
    from finite_ecd import sensor_repair as mech_sensor_repair
    from finite_ecd import verify_sensor_repair as mech_verify_sensor_repair
    from finite_ecd import td_dynamic_program as mdp
    from finite_ecd import verify_dp_certificate as mverify_dp

    tb_model = mgen.ten_bar_model()
    tb_batch = mechanics_fe.generate(tb_model)
    tb_verify = mechanics_fe.verify(tb_model, tb_batch)
    tb_bad = json.loads(json.dumps(tb_batch))
    tb_bad["rows"][0]["constant"] = "999999"
    tb_bad_verify = mechanics_fe.verify(tb_model, tb_bad)

    mech_smoke = {}
    for obs in ("same", "split"):
        inst_raw = mgen.build_instance(tb_model, tb_batch, obs)
        dec = mgen.min_fill_decomp(inst_raw)
        inst = MInstance.from_json(inst_raw)
        ok_td, _ = mvalidate_td(inst, dec)
        cert = mdp(inst, inst_raw, dec)
        ok_dp, _ = mverify_dp(inst, inst_raw, cert)
        mech_smoke[obs] = {
            "tree_decomp_verify": "VERIFIED" if ok_td else "REJECTED",
            "dp_type": cert["type"],
            "dp_status": cert["status"],
            "dp_verify": "VERIFIED" if ok_dp else "REJECTED",
        }

    tb_sensor_data = mgen.ten_bar_sensor_data(tb_model, tb_batch)
    tb_repair = mech_sensor_repair(tb_sensor_data["actions"], tb_sensor_data["scenarios"], tb_sensor_data["sensors"])
    tb_repair_verify = mech_verify_sensor_repair(tb_sensor_data["actions"], tb_sensor_data["scenarios"],
                                                   tb_sensor_data["sensors"], tb_repair)
    (ROOT / "examples/mech_ten_bar_smoke_sensors.json").write_text(json.dumps(tb_sensor_data, indent=2))
    (ROOT / "examples/mech_ten_bar_smoke_sensor_repair.json").write_text(json.dumps(tb_repair, indent=2))

    ch_model = mgen.chain_pretension_model(16)
    ch_batch = mechanics_fe.generate(ch_model)
    ch_verify = mechanics_fe.verify(ch_model, ch_batch)
    ch_inst_raw = mgen.build_instance(ch_model, ch_batch, "same")
    ch_dec = mgen.min_fill_decomp(ch_inst_raw)
    ch_inst = MInstance.from_json(ch_inst_raw)
    ch_cert = mdp(ch_inst, ch_inst_raw, ch_dec)
    ch_ok_dp, _ = mverify_dp(ch_inst, ch_inst_raw, ch_cert)

    report = {
        "generator": {"returncode": gen.returncode, "stdout": gen.stdout, "stderr": gen.stderr},
        "mechanics_ten_bar": {
            "row_batch_verify": "VERIFIED" if tb_verify[0] else "REJECTED",
            "corrupted_row_batch_verify": "REJECTED" if not tb_bad_verify[0] else "VERIFIED",
            "same_observation": mech_smoke["same"],
            "split_observation": mech_smoke["split"],
            "sensor_repair_status": tb_repair.get("status"),
            "sensor_repair_verify": "VERIFIED" if tb_repair_verify[0] else "REJECTED",
        },
        "mechanics_chain16": {
            "row_batch_verify": "VERIFIED" if ch_verify[0] else "REJECTED",
            "dp_type": ch_cert["type"],
            "dp_status": ch_cert["status"],
            "dp_verify": "VERIFIED" if ch_ok_dp else "REJECTED",
        },
        "same_observation": same,
        "split_observation": split,
        "fibre_conflict_verify": fibre_verify,
        "bad_fibre_conflict_verify": bad_fibre_verify,
        "sensor_repair": sensor,
        "sensor_repair_verify": sensor_verify,
        "bad_sensor_repair_verify": bad_sensor_verify,
        "tree_decomp_verify": tree_decomp_verify,
        "dp_optimum": {"type": dp_opt.get("type"), "status": dp_opt.get("status"), "optimum_cost": dp_opt.get("optimum_cost")},
        "dp_optimum_verify": dp_opt_verify,
        "dp_refutation": {"type": dp_ref.get("type"), "status": dp_ref.get("status"), "optimum_cost": dp_ref.get("optimum_cost")},
        "dp_refutation_verify": dp_ref_verify,
        "bad_dp_verify": bad_dp_verify,
        "fe_rows": {"type": fe_rows.get("type"), "status": fe_rows.get("status"), "row_count": len(fe_rows.get("rows", []))},
        "fe_rows_verify": fe_verify,
        "bad_fe_rows_verify": bad_fe_verify,
        "sparsification": {"type": spars.get("type"), "status": spars.get("status"), "row_count": len(spars.get("rows", []))},
        "sparsification_verify": spars_verify,
        "bad_sparsification_verify": bad_spars_verify,
        "path_tree_decomp_verify": path_td_verify,
        "path_dp_optimum": {"type": path_dp.get("type"), "status": path_dp.get("status"), "optimum_cost": path_dp.get("optimum_cost")},
        "path_dp_optimum_verify": path_dp_verify,
        "path_dp_refutation": {"type": path_ref.get("type"), "status": path_ref.get("status")},
        "path_dp_refutation_verify": path_ref_verify,
        "baseline_dimacs": {"returncode": dimacs["returncode"], "bytes": len(dimacs["stdout"])},
        "baseline_milp_lp": {"returncode": milp["returncode"], "bytes": len(milp["stdout"])},
        "baseline_cpsat_json": {"returncode": cpsat["returncode"], "bytes": len(cpsat["stdout"])},
        "external_missing_solver": json.loads(missing_solver["stdout"]),
        "generated_path6": {"generator_returncode": gen_path["returncode"], "td_verify": gen_path_td_verify, "dp_status": gen_path_dp.get("status"), "dp_verify": gen_path_dp_verify},
        "generated_binary_tree_depth2": {"generator_returncode": gen_tree["returncode"], "td_verify": gen_tree_td_verify, "dp_status": gen_tree_dp.get("status"), "dp_verify": gen_tree_dp_verify},
        "sparsification_ladder_verify": ladder_verify,
        "four_actuator_frame": {"fe_verify": frame_verify, "dp_status": frame_dp.get("status"), "dp_type": frame_dp.get("type"), "dp_verify": frame_dp_verify},
        "external_cross_check_sat": json.loads(cross_sat["stdout"]),
        "external_cross_check_unsat": json.loads(cross_unsat["stdout"]),
        "external_cross_check_no_cert": json.loads(cross_sat_nocert["stdout"]),
        "generated_band7_w2": {"generator_returncode": band_gen["returncode"], "td_verify": band_td, "dp_status": band_dp.get("status"), "dp_verify": band_dp_verify},
        "generated_grid2x4": {"generator_returncode": grid_gen["returncode"], "td_verify": grid_td, "dp_status": grid_dp.get("status"), "dp_verify": grid_dp_verify},
        "grid2x4_summary": json.loads(grid_summary["stdout"]),
        "expected_gate": {
            "same_observation": "CERTIFIED-UNSAT",
            "split_observation": "CERTIFIED-SAT",
            "fibre_conflict_verify": "VERIFIED",
            "bad_fibre_conflict_verify": "REJECTED",
            "sensor_repair": "CERTIFIED-OPT",
            "sensor_repair_verify": "VERIFIED",
            "bad_sensor_repair_verify": "REJECTED",
            "tree_decomp_verify": "VERIFIED",
            "dp_optimum": "DP-OPTIMUM/CERTIFIED-OPT/3",
            "dp_optimum_verify": "VERIFIED",
            "dp_refutation": "DP-REFUTATION/CERTIFIED-UNSAT",
            "dp_refutation_verify": "VERIFIED",
            "bad_dp_verify": "REJECTED",
            "fe_rows_verify": "VERIFIED",
            "bad_fe_rows_verify": "REJECTED",
            "sparsification_verify": "VERIFIED",
            "bad_sparsification_verify": "REJECTED",
            "path_tree_decomp_verify": "VERIFIED",
            "path_dp_optimum": "DP-OPTIMUM/CERTIFIED-OPT/1",
            "path_dp_optimum_verify": "VERIFIED",
            "path_dp_refutation": "DP-REFUTATION/CERTIFIED-UNSAT",
            "path_dp_refutation_verify": "VERIFIED",
            "baseline_encoders": "returncode 0",
            "external_missing_solver": "INCONCLUSIVE",
            "generated_path6": "VERIFIED",
            "generated_binary_tree_depth2": "VERIFIED",
            "sparsification_ladder_verify": "VERIFIED",
            "four_actuator_frame": "VERIFIED",
            "external_cross_check_sat": "VERIFIED-SAT",
            "external_cross_check_unsat": "VERIFIED-UNSAT",
            "external_cross_check_no_cert": "INCONCLUSIVE",
            "generated_band7_w2": "VERIFIED",
            "generated_grid2x4": "VERIFIED",
            "grid2x4_summary": "VERIFIED",
            "mechanics_ten_bar_row_batch_verify": "VERIFIED",
            "mechanics_ten_bar_corrupted_row_batch_verify": "REJECTED",
            "mechanics_ten_bar_same_observation": "DP-REFUTATION/CERTIFIED-UNSAT",
            "mechanics_ten_bar_split_observation": "DP-OPTIMUM/CERTIFIED-OPT",
            "mechanics_ten_bar_sensor_repair": "CERTIFIED-OPT",
            "mechanics_ten_bar_sensor_repair_verify": "VERIFIED",
            "mechanics_chain16_row_batch_verify": "VERIFIED",
            "mechanics_chain16_dp": "DP-REFUTATION/CERTIFIED-UNSAT"
        }
    }
    out = ROOT / "repro_report.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
