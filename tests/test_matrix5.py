import sympy as sp
from examples.matrix5_solution import A, B, EXPECTED, cell_work, build_solution


def test_all_25_cells_and_every_intermediate_value():
    independent = sp.Matrix(A) * sp.Matrix(B)
    assert independent == sp.Matrix(EXPECTED)
    assert len(A) == len(B) == 5
    multiplications = additions = 0
    for i in range(5):
        for j in range(5):
            products, totals = cell_work(i, j)
            for k in range(5):
                assert products[k] == A[i][k] * B[k][j]
                assert totals[k] == sum(A[i][t] * B[t][j] for t in range(k + 1))
                multiplications += 1
                additions += int(k > 0)
            assert totals[-1] == independent[i, j]
    assert (multiplications, additions) == (125, 100)
    solution = build_solution()
    assert len(solution.steps) == 26
    assert len(solution.checks) == 276
    assert all(check.status == 'passed' for check in solution.checks)


def test_first_and_last_cell_have_signed_and_zero_terms():
    assert cell_work(0, 0) == ([2, -2, -3, 0, 12], [2, 0, -3, -3, 9])
    assert cell_work(4, 4) == ([0, 12, 2, 2, -5], [0, 12, 14, 16, 11])
