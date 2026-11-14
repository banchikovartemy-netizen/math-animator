import sympy as sp
from explanation.model import Solution,Step
from math_engine.checks import identity
x,y,t=sp.symbols('x y t',real=True)
A=sp.Matrix([[2,1],[1,-1]])
b=sp.Matrix([5,1])
ANSWER=sp.Matrix([2,1])
AUGMENTED=[sp.Matrix([[2,1,5],[1,-1,1]]),sp.Matrix([[1,-1,1],[2,1,5]]),sp.Matrix([[1,-1,1],[0,3,3]])]

def build_solution():
    checks=[identity('Проверка исходной системы',A*ANSWER,b),
      identity('Независимое символьное решение',sp.Matrix(sp.linsolve((A,b)).args[0]),ANSWER),
      identity('Подстановка: раскрытие скобок',2*(y+1)+y,3*y+2),
      identity('Подстановка: y=1',sp.Integer(3)*1+2,sp.Integer(5)),
      identity('Сложение: исключение y',(2*x+y)+(x-y),3*x),
      identity('Сложение: сумма правых частей',sp.Integer(5)+1,sp.Integer(6)),
      identity('Определитель D',A.det(),sp.Integer(-3)),
      identity('Определитель Dx',sp.Matrix([[5,1],[1,-1]]).det(),sp.Integer(-6)),
      identity('Определитель Dy',sp.Matrix([[2,5],[1,1]]).det(),sp.Integer(-3)),
      identity('Крамер x',sp.Rational(-6,-3),sp.Integer(2)),
      identity('Крамер y',sp.Rational(-3,-3),sp.Integer(1)),
      identity('Обратная матрица',A.inv(),sp.Rational(-1,3)*sp.Matrix([[-1,-1],[-1,2]])),
      identity('A A⁻¹ = I',A*A.inv(),sp.eye(2)),
      identity('Матричный ответ',A.inv()*b,ANSWER)]
    swap=AUGMENTED[0].copy();swap.row_swap(0,1)
    checks.append(identity('Гаусс: перестановка строк',swap,AUGMENTED[1]))
    reduced=swap.copy();reduced[1,:]=reduced[1,:]-2*reduced[0,:]
    checks.append(identity('Гаусс: R2−2R1',reduced,AUGMENTED[2]))
    checks.append(identity('Гаусс: итог RREF',A.row_join(b).rref()[0],sp.Matrix([[1,0,2],[0,1,1]])))
    for px,py in [(0,5),(2,1)]:checks.append(identity(f'Точка первой прямой ({px},{py})',sp.Integer(2*px+py),sp.Integer(5)))
    for px,py in [(0,-1),(2,1)]:checks.append(identity(f'Точка второй прямой ({px},{py})',sp.Integer(px-py),sp.Integer(1)))
    singular=sp.Matrix([[2,1],[4,2]])
    checks += [identity('Вырожденная матрица: ранг 1',sp.Integer(singular.rank()),sp.Integer(1)),
               identity('Несовместная система: ранг расширенной матрицы 2',sp.Integer(singular.row_join(sp.Matrix([5,11])).rank()),sp.Integer(2)),
               identity('Совпадающие прямые: ранг расширенной матрицы 1',sp.Integer(singular.row_join(sp.Matrix([5,10])).rank()),sp.Integer(1)),
               identity('Параметрическое бесконечное семейство',singular*sp.Matrix([t,5-2*t]),sp.Matrix([5,10]))]
    return Solution('Решить 2x+y=5, x−y=1 шестью основными методами.',
       'Сравнить методы и получить проверенное решение (2,1)',
       'Подстановка, сложение, графический метод, Крамер, Гаусс, обратная матрица',
       'x,y∈R; линейная система 2×2; D=−3≠0; решение единственно',[
       Step('Выразить x=y+1; подставить и решить',['2(y+1)+y=5','3y+2=5','3y=3','y=1','x=2'],'Перенос выражения из второй строки в первую','TransformFromCopy'),
       Step('Сложить уравнения и исключить y',['(2x+y)+(x-y)=5+1','3x=6','x=2','y=1'],'Выделить взаимное уничтожение y и −y','Indicate'),
       Step('Построить две прямые',['y=5-2x','y=x-1','(x,y)=(2,1)'],'Оси, опорные точки, пересечение','Create'),
       Step('Вычислить три определителя',['D=-3','D_x=-6','D_y=-3','x=D_x/D=2','y=D_y/D=1'],'Выделить заменённые столбцы','SurroundingRectangle'),
       Step('Прямой ход Гаусса и обратная подстановка',['R_1↔R_2','R_2←R_2-2R_1','3y=3','x-y=1'],'Преобразования расширенной матрицы','ReplacementTransform'),
       Step('Использовать обратную матрицу',['AX=b','X=A^{-1}b','A^{-1}=(-1/3)[[-1,-1],[-1,2]]','X=(2,1)^T'],'Преобразование матричных формул','TransformMatchingTex'),
       Step('Различать единственное, отсутствующее и бесконечное множество решений',['0=1','0=0','(x,y)=(t,5-2t)'],'Три сравниваемые системы','Write'),
       Step('Проверить ответ и выбрать метод',['2·2+1=5','2-1=1'],'Сравнение условий применимости','FadeIn')],checks)
