import sympy as sp
from examples.integral_graph_solution import F,x,POINTS,build_solution


def test_integral_and_all_features():
    assert sp.diff(F,x)==x**2-4
    assert sp.diff(F,x,2).subs(x,-2)<0
    assert sp.diff(F,x,2).subs(x,2)>0
    assert F.subs(x,-2)==sp.Rational(16,3)
    assert F.subs(x,2)==sp.Rational(-16,3)
    assert all(F.subs(x,a)==b for a,b in POINTS)
    assert set(sp.solve(F,x))=={-2*sp.sqrt(3),0,2*sp.sqrt(3)}
    assert all(check.status=='passed' for check in build_solution().checks)
