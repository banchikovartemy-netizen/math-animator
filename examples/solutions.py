import sympy as sp
from math_engine.checks import Check, identity
from explanation.model import Solution, Step

def make(kind):
    x=sp.Symbol('x',real=True)
    if kind=='integration':
        checks=[identity('Производная первообразной равна подынтегральной функции',sp.diff(sp.exp(x)*(x-1),x),x*sp.exp(x),domain='x ∈ R')]
        return Solution('Найти интеграл x exp(x) dx','Первообразная','Интегрирование по частям','x ∈ R; C ∈ R',[
            Step('Выбор u и dv',[r'u=x',r'dv=e^x dx'],'Выделить множители','Write'),
            Step('Применить формулу по частям',[r'xe^x-\int e^x dx'],'Преобразовать общие части','TransformMatchingTex'),
            Step('Вычислить и проверить',[r'e^x(x-1)+C'],'Рамка ответа и производная','Create')],checks)
    if kind=='derivative':
        f=x**3-3*x
        checks=[identity('Производная',sp.diff(f,x),3*x*x-3),identity('Критические точки',sp.Matrix(sp.solve(sp.diff(f,x),x)),sp.Matrix([-1,1])),identity('Значения экстремумов',sp.Matrix([f.subs(x,-1),f.subs(x,1)]),sp.Matrix([2,-2])),identity('Вторая производная в критических точках',sp.Matrix([sp.diff(f,x,2).subs(x,-1),sp.diff(f,x,2).subs(x,1)]),sp.Matrix([-6,6]))]
        return Solution('Исследовать f(x)=x³−3x','Производная и экстремумы','Знак производной; вторая производная','x ∈ R',[Step('f′=3x²−3; нули ±1',['f(x)=x^3-3x',"f'(x)=3x^2-3"],'Графики f и f′; движущаяся касательная','Create'),Step('Максимум (-1,2), минимум (1,-2)',[],'Выделить критические точки','FadeIn')],checks)
    if kind=='geometry':
        checks=[identity('Гипотенуза',sp.sqrt(3**2+4**2),sp.Integer(5)),identity('Площадь',sp.Rational(1,2)*3*4,sp.Integer(6)),identity('Перпендикулярность катетов',sp.Matrix([4,0]).dot(sp.Matrix([0,3])),sp.Integer(0))]
        return Solution('Катеты прямоугольного треугольника 3 и 4. Найти гипотенузу и площадь','Длина и площадь','Теорема Пифагора; достроение прямоугольника','Евклидова плоскость; длины положительны',[Step('c²=25, c=5',['c=5'],'Построить треугольник с прямым углом','Create'),Step('Половина прямоугольника',['S=6'],'Достроить второй треугольник','Create')],checks)
    if kind=='matrix':
        checks=[identity('Произведение матриц',sp.Matrix([[1,2],[3,4]])*sp.Matrix([[2,0],[1,3]]),sp.Matrix([[4,6],[10,12]]))]
        return Solution('Перемножить матрицы [[1,2],[3,4]] и [[2,0],[1,3]]','Матрица произведения','Скалярные произведения строк и столбцов','Матрицы 2×2 над R',[Step('Вычислить четыре ячейки',[],'Подсвечивать соответствующие строки и столбцы','SurroundingRectangle')],checks)
    if kind=='graph':
        from collections import deque
        adjacency={1:[2,3],2:[1,4],3:[1,4],4:[2,3,5],5:[4]}
        distances={1:0};queue=deque([1])
        while queue:
            v=queue.popleft()
            for w in adjacency[v]:
                if w not in distances:distances[w]=distances[v]+1;queue.append(w)
        checks=[Check('Кратчайшее расстояние 1 → 5 равно 3','passed' if distances[5]==3 else 'failed','Независимый BFS',str(distances))]
        return Solution('Найти кратчайший путь 1 → 5 в графе с рёбрами 12,13,24,34,45','Путь и расстояние','Обход в ширину','Конечный простой неориентированный невзвешенный граф',[Step('Раскрыть слои BFS',[],'Подсветить слои и путь длины 3','Цвет рёбер')],checks)
    raise ValueError(kind)
