"""Worked solutions for the Exam 2 and Final study guides.

Same schema and same guarantees as `exam1_sol.py`: every entry carries the steps,
a named trap, and a `check` that re-derives the answer with sympy at build time.
The Exam 1 bank stayed in its own file because it is hand-written and heavily
annotated; these were produced in five parallel passes over the official guides
and are merged here.

`exam1_sol.verify()` and `exam1_audit.gate()` both run over the merged bank, so a
solution here is held to exactly the same standard: a check that disagrees with
its own `want` stops the build, and a `want` that disagrees with the instructor's
printed answer stops the build unless it carries a documented `fix`.
"""

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = ["sol_A", "sol_B", "sol_C", "sol_D", "sol_E"]

SOL = {}


def _load(name):
    path = HERE / "solutions" / f"{name}.py"
    if not path.exists():
        sys.exit(f"exam2_sol: {path} missing — the solution batch was not merged")
    spec = importlib.util.spec_from_file_location(f"_ma261_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SOL


for _part in PARTS:
    _batch = _load(_part)
    _clash = set(_batch) & set(SOL)
    if _clash:
        sys.exit(f"exam2_sol: {_part} redefines {sorted(_clash)}")
    SOL.update(_batch)
