import sympy as sp
from explanation.model import Solution,Step
from math_engine.checks import identity,Check
x=sp.Symbol('x',real=True)
F=x**3/3-4*x
POINTS=[(-4,sp.Rational(-16,3)),(-2,sp.Rational(16,3)),(0,0),(2,sp.Rational(-16,3)),(4,sp.Rational(16,3))]

def build_solution():
    checks=[identity('Производная первообразной',sp.diff(F,x),x*x-4),
            identity('Критические точки',sp.Matrix(sp.solve(sp.diff(F,x),x)),sp.Matrix([-2,2])),
            identity('Вторая производная',sp.diff(F,x,2),2*x),
            identity('F″(-2)=-4 < 0: максимум',sp.diff(F,x,2).subs(x,-2),sp.Integer(-4)),
            identity('F″(2)=4 > 0: минимум',sp.diff(F,x,2).subs(x,2),sp.Integer(4)),
            identity('Нули функции',sp.Matrix(sorted(sp.solve(F,x),key=lambda v:float(v))),sp.Matrix([-2*sp.sqrt(3),0,2*sp.sqrt(3)])),
            identity('Точка перегиба',sp.solve(sp.diff(F,x,2),x)[0],sp.Integer(0))]
    for a,b in POINTS:checks.append(identity(f'Опорная точка F({a})',F.subs(x,a),sp.sympify(b)))
    # Algebraic sign reasoning: x²−4=(x−2)(x+2); signs on open intervals.
    checks += [Check('Рост вне [-2,2], убывание внутри','passed','Знаки линейных множителей (x−2)(x+2)','Оба положительны при x>2; оба отрицательны при x<−2; разные знаки при −2<x<2.'),
               Check('Смена выпуклости в нуле','passed','Знак F″(x)=2x','F″<0 слева от 0 и >0 справа; F(0)=0.')]
    return Solution('Вычислить ∫(x²−4)dx и исследовать график первообразной при C=0.',
      'Первообразная, максимум, минимум, перегиб, нули и график',
      'Линейность интеграла; степенная формула; первая и вторая производные','x∈R; C∈R; для выбранного графика C=0',[
      Step('Интегрируем слагаемые и проверяем производной',[r'\int(x^2-4)dx=\frac{x^3}{3}-4x+C'],'Преобразования формулы, выделение результата','TransformMatchingTex'),
      Step('Для C=0 находим критические точки',[r"F'(x)=x^2-4=0",r'x=\pm2'],'Числовая прямая, знаки производной','Create'),
      Step('Вычисляем оба экстремума',[r'F(-2)=16/3',r'F(2)=-16/3',r"F''(-2)=-4<0",r"F''(2)=4>0"],'Подстановка чисел и классификация','ReplacementTransform'),
      Step('Вычисляем опорные точки',[r'F(-4)=-16/3',r'F(-2)=16/3',r'F(0)=0',r'F(2)=-16/3',r'F(4)=16/3'],'Подстановки, точки и аналитическая кривая','Create'),
      Step('Перегиб и нули',[r"F''(x)=2x=0",r'x=0',r'F(x)=x(x^2-12)/3=0',r'x=0,\pm2\sqrt3'],'Выделение перегиба и пересечений оси','FadeIn'),
      Step('Итоговая карта графика',[],'График, максимум, минимум и перегиб','Create')],checks)
