#!/usr/bin/env python3
"""Generate exact two-spring finite ECD instances.

Model: u(f,a1,a2) = (f-a1-a2)/2, f in {1,2}, a1,a2 in {0,1}, safe iff |u| <= 0.25.
"""
from __future__ import annotations
import json
from pathlib import Path

ACTIONS = [[0,0], [0,1], [1,0], [1,1]]

def safe_actions(f: int):
    out=[]
    for a1,a2 in ACTIONS:
        u=(f-a1-a2)/2
        if abs(u) <= 0.25:
            out.append([a1,a2])
    return out

def main():
    out=Path(__file__).parent / "examples"
    out.mkdir(exist_ok=True)
    same={
      "variables": ["cmd"],
      "domains": {"cmd": ACTIONS},
      "factors": [
        {"name": "load_1", "scope": ["cmd"], "relation": [[a] for a in safe_actions(1)]},
        {"name": "load_2", "scope": ["cmd"], "relation": [[a] for a in safe_actions(2)]}
      ]
    }
    split={
      "variables": ["cmd_low", "cmd_high"],
      "domains": {"cmd_low": ACTIONS, "cmd_high": ACTIONS},
      "factors": [
        {"name": "load_1", "scope": ["cmd_low"], "relation": [[a] for a in safe_actions(1)]},
        {"name": "load_2", "scope": ["cmd_high"], "relation": [[a] for a in safe_actions(2)]}
      ]
    }
    (out/"generated_two_spring_same.json").write_text(json.dumps(same, indent=2))
    (out/"generated_two_spring_split.json").write_text(json.dumps(split, indent=2))
    print(json.dumps({"R1": safe_actions(1), "R2": safe_actions(2)}, indent=2))

if __name__ == "__main__":
    main()
