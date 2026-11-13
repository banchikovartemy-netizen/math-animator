"""Exact, reviewed data and arithmetic for this particular 5×5 problem."""
import sympy as sp
from explanation.model import Solution, Step
from math_engine.checks import identity

A = [
    [2, -1, 3, 0, 4],
    [1, 5, -2, 3, 1],
    [0, 2, 4, -1, 3],
    [3, 1, 0, 2, -2],
    [-1, 4, 2, 1, 5],
]
B = [
    [1, 3, -1, 2, 0],
    [2, -2, 4, 1, 3],
    [-1, 0, 2, 5, 1],
    [4, 1, 0, -2, 2],
    [3, 2, 1, 0, -1],
]
# Independently written expected answer; never derived by the animation.
EXPECTED = [
    [9, 16, 4, 18, -4],
    [28, -2, 16, -9, 18],
    [5, 1, 19, 24, 5],
    [7, 5, -1, 3, 9],
    [24, 0, 26, 10, 11],
]

def signed(value):
    return f'({value})' if value < 0 else str(value)

def cell_work(i, j):
    products = [A[i][k] * B[k][j] for k in range(5)]
    totals = []
    total = 0
    for product in products:
        total += product
        totals.append(total)
    return products, totals

def build_solution():
    symbolic = sp.Matrix(A) * sp.Matrix(B)
    checks = [identity('Полное произведение A B', symbolic, sp.Matrix(EXPECTED))]
    steps = [Step('Пять столбцов A совпадают с пятью строками B: произведение определено.',
                  [r'C=AB', r'c_{ij}=\sum_{k=1}^{5}a_{ik}b_{kj}'],
                  'Три матрицы; результат заполняется по строкам', 'Write')]
    for i in range(5):
        for j in range(5):
            products, totals = cell_work(i, j)
            for k in range(5):
                checks.append(identity(f'c[{i+1},{j+1}], произведение {k+1}',
                                       sp.Integer(products[k]), sp.Integer(A[i][k])*sp.Integer(B[k][j])))
                checks.append(identity(f'c[{i+1},{j+1}], накопленная сумма {k+1}',
                                       sp.Integer(totals[k]),
                                       sum((sp.Integer(A[i][t])*sp.Integer(B[t][j]) for t in range(k+1)), sp.Integer(0))))
            checks.append(identity(f'Элемент c[{i+1},{j+1}] совпадает с SymPy',sp.Integer(totals[-1]),symbolic[i,j]))
            expansion = '+'.join(f'{signed(A[i][k])}\\cdot{signed(B[k][j])}' for k in range(5))
            arithmetic = [f'{signed(A[i][k])}\\cdot{signed(B[k][j])}={products[k]}' for k in range(5)]
            sums = [f's_1={products[0]}'] + [f's_{k+1}={signed(totals[k-1])}+{signed(products[k])}={totals[k]}' for k in range(1,5)]
            steps.append(Step(f'Строка {i+1} матрицы A × столбец {j+1} матрицы B; c[{i+1},{j+1}]={totals[-1]}.',
                              [f'c_{{{i+1}{j+1}}}={expansion}={totals[-1]}',*arithmetic,*sums],
                              'Выделить строку и столбец, затем каждую пару; считать произведение и сумму; перенести итог в C',
                              'SurroundingRectangle, Indicate, TransformFromCopy, ReplacementTransform'))
    return Solution('Вычислить AB для двух указанных целочисленных матриц 5×5.',
                    'Все 25 элементов произведения с полной арифметикой',
                    'Строка на столбец; пять произведений и четыре сложения для каждой ячейки',
                    'A,B ∈ Z^(5×5); произведение определено, результат 5×5',steps,checks)
