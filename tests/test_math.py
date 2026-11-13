import pytest
import sympy as sp
from examples.solutions import make
from math_engine.checks import identity, require_passed

@pytest.mark.parametrize("job", ["integration", "derivative", "geometry", "matrix", "graph"])
def test_reviewed_examples(job):
    solution = make(job)
    assert solution.domain and solution.method and solution.steps
    assert solution.checks and all(c.status == "passed" for c in solution.checks)

def test_wrong_result_fails():
    x = sp.Symbol("x", real=True)
    check = identity("wrong primitive", sp.diff(x**2, x), 3*x)
    assert check.status == "failed"
    with pytest.raises(ValueError): require_passed([check])

def test_undecidable_result_is_not_proof():
    x = sp.Symbol("x")
    check = identity("unknown", sp.Function("f")(x), 0)
    assert check.status == "unverified"

def test_matrix_mismatch_fails():
    check = identity("wrong matrix", sp.eye(2), sp.zeros(2))
    assert check.status == "failed"
