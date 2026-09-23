#!/usr/bin/env python3
"""Dependency-free baseline encoders for tiny Boolean explicit-table instances.

These encoders are for fair-instance generation only. They do not solve the
encoded instances and do not support non-Boolean domains.
"""
from __future__ import annotations
import argparse, itertools, json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load(path):
    return json.loads(Path(path).read_text())


def ensure_bool(data):
    for x in data["variables"]:
        if set(data["domains"][x]) != {0,1}:
            raise ValueError(f"{x} is not Boolean with domain [0,1]")


def forbidden_tuples(data):
    out=[]
    for f in data.get("factors",[]):
        scope=f["scope"]
        allowed={tuple(row) for row in f["relation"]}
        for vals in itertools.product([0,1], repeat=len(scope)):
            if vals not in allowed:
                out.append((f["name"], scope, vals))
    return out


def to_dimacs(data):
    ensure_bool(data)
    varnum={x:i+1 for i,x in enumerate(data["variables"])}
    clauses=[]
    comments=[]
    for name,scope,vals in forbidden_tuples(data):
        clause=[]
        for x,v in zip(scope, vals):
            # clause says at least one variable differs from forbidden tuple
            clause.append(-varnum[x] if v==1 else varnum[x])
        clauses.append(clause)
        comments.append(f"c forbid {name} {dict(zip(scope, vals))}")
    lines=[f"c var {i} {x}" for x,i in varnum.items()]
    lines+=comments
    lines.append(f"p cnf {len(varnum)} {len(clauses)}")
    lines += [" ".join(map(str,c))+" 0" for c in clauses]
    return "\n".join(lines)+"\n"


def to_milp_lp(data):
    ensure_bool(data)
    lines=["\\ Boolean forbidden-tuple encoding", "Minimize", " obj: 0", "Subject To"]
    k=0
    for name,scope,vals in forbidden_tuples(data):
        terms=[]
        const=0
        for x,v in zip(scope, vals):
            if v==0:
                terms.append(f"+ {x}")
            else:
                terms.append(f"- {x}"); const += 1
        # const + terms >= 1
        rhs=1-const
        lines.append(f" c{k}_{name}: " + " ".join(terms).lstrip('+ ') + f" >= {rhs}")
        k+=1
    lines.append("Binary")
    for x in data["variables"]: lines.append(f" {x}")
    lines.append("End")
    return "\n".join(lines)+"\n"


def to_cpsat_json(data):
    ensure_bool(data)
    return {
        "format": "minimal-cpsat-forbidden-tuples",
        "variables": [{"name": x, "domain": [0,1]} for x in data["variables"]],
        "forbidden_assignments": [
            {"name": name, "scope": scope, "tuple": list(vals)}
            for name, scope, vals in forbidden_tuples(data)
        ]
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("format", choices=["dimacs","milp-lp","cpsat-json"])
    ap.add_argument("instance")
    args=ap.parse_args()
    data=load(args.instance)
    if args.format=="dimacs": print(to_dimacs(data), end="")
    elif args.format=="milp-lp": print(to_milp_lp(data), end="")
    else: print(json.dumps(to_cpsat_json(data), indent=2))

if __name__=="__main__": main()
