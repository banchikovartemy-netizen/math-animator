import sympy as sp
from explanation.model import Solution,Step
from math_engine.checks import identity
TOTAL=1000
COUNTS=[100,333,2,565]
PERCENTAGES=[sp.Rational(n,10) for n in COUNTS]

def build_solution():
    checks=[identity('Исходная сумма равна 1100',sp.Integer(100+333+2+665),sp.Integer(1100)),
            identity('Избыток исходного задания равен 100',sp.Integer(1100-TOTAL),sp.Integer(100)),
            identity('Остаток для склада',sp.Integer(TOTAL-100-333-2),sp.Integer(565)),
            identity('В итоговом распределении ровно 1000 человек',sp.Integer(sum(COUNTS)),sp.Integer(TOTAL)),
            identity('Сумма долей равна 100%',sum(PERCENTAGES),sp.Integer(100))]
    for n,p in zip(COUNTS,PERCENTAGES):checks.append(identity(f'Доля группы {n}',100*sp.Rational(n,TOTAL),p))
    return Solution('Распределить 1000 человек: 100 учёных, 333 работника на ПК, 2 администратора; остальных — на склад.',
        'Согласованное распределение 1000 человек',
        'Вычитание фиксированных групп из общего количества; проверка суммы и процентов',
        'Количество людей — неотрицательные целые числа; группы не пересекаются',[
        Step('Исходные числа давали 1100, а не 1000',['100+333+2+665=1100'],'Показать превышение полосы вместимости','Create'),
        Step('По уточнению пользователя пересчитываем склад',['1000-100-333-2=565'],'Уменьшить склад на 100','Transform'),
        Step('Проверяем итог и проценты',['100+333+2+565=1000','10+33.3+0.2+56.5=100'],'Полоса и подписи всех групп','Write')],checks)
