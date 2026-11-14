import sympy as sp
from examples.quadratic_data import A,B,C
from explanation.model import Solution,Step
from math_engine.checks import identity

def build_solution():
    a,b,c=[sp.Rational(str(v)) for v in (A,B,C)]
    if a==0:raise ValueError('A must be nonzero')
    x=sp.Symbol('x')
    p=a*x*x+b*x+c;D=b*b-4*a*c
    roots=[sp.simplify((-b+s*sp.sqrt(D))/(2*a)) for s in (1,-1)]
    checks=[identity('Дискриминант',D,sp.discriminant(p,x)),
            identity('Степень многочлена равна 2',sp.Integer(sp.degree(p,x)),sp.Integer(2)),
            identity('Первый корень: подстановка',p.subs(x,roots[0]),sp.Integer(0)),
            identity('Второй корень: подстановка',p.subs(x,roots[1]),sp.Integer(0)),
            identity('Сумма корней по Виету',sum(roots),-b/a),
            identity('Произведение корней по Виету',roots[0]*roots[1],c/a),
            identity('Разложение исходного многочлена',sp.expand(a*(x-roots[0])*(x-roots[1])),p)]
    return Solution(f'Решить ({a})x²+({b})x+({c})=0',
        'Корни квадратного уравнения','Дискриминант и формула корней',
        'a≠0; коэффициенты рациональные; при D<0 корни рассматриваются в C',[
        Step('Вычислить дискриминант',['D=b^2-4ac',f'D={sp.latex(D)}'],'Преобразовать формулу с подстановкой коэффициентов','TransformMatchingTex'),
        Step('Определить число действительных корней',[],'Объяснить знак дискриминанта','FadeIn'),
        Step('Вычислить корни',[f'x_1={sp.latex(roots[0])}',f'x_2={sp.latex(roots[1])}'],'Подставить числа в формулу корней','Write'),
        Step('Проверить подстановкой и по Виету',[],'Выделить проверенный ответ рамкой','Create')],checks)
