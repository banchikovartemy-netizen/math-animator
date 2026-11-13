"""Checks consume reviewed SymPy objects, never parse user text as code."""
from dataclasses import dataclass, asdict
import sympy as sp

@dataclass(frozen=True)
class Check:
    claim: str
    status: str
    method: str
    detail: str = ""
    def as_dict(self):
        return asdict(self)

def identity(claim, left, right, *, method="symbolic simplification", domain=""):
    difference = left - right
    if isinstance(difference, sp.MatrixBase):
        values = [sp.simplify(v) for v in difference]
    else:
        values = [sp.simplify(difference)]
    if all(v == 0 for v in values):
        status = "passed"
    elif any(v.is_zero is False or (v.free_symbols and v.is_polynomial(*v.free_symbols) and v != 0) for v in values):
        status = "failed"
    else:
        status = "unverified"
    return Check(claim, status, method, domain)

def require_passed(checks):
    failed = [c.claim for c in checks if c.status == "failed"]
    if failed:
        raise ValueError("Mathematical checks failed: " + "; ".join(failed))
