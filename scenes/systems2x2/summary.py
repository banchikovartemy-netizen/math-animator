from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Summary(SystemsBase):
    def construct(self):
        self.heading('Как выбрать метод?')
        rows=[('Подстановка','Переменную легко выразить'),('Сложение','Удобно исключить одну переменную'),('График','Нужен геометрический смысл'),('Крамер','Небольшая квадратная система, D ≠ 0'),('Гаусс','Общий метод, выявляет совместность'),('Обратная матрица','Квадратная система, det A ≠ 0')]
        for i,(method,usage) in enumerate(rows):
            left=Text(method,font='DejaVu Sans',font_size=24,color=ManimColor(ACCENT))
            self.fit(left,width=4,height=.45);left.move_to([-4,2.35-i*.72,0])
            right=Text(usage,font='DejaVu Sans',font_size=22)
            self.fit(right,width=7.4,height=.45);right.move_to([2,2.35-i*.72,0])
            self.check_frame(left,right);self.play(FadeIn(left),FadeIn(right),run_time=.35)
        answer=self.eq('(x,y)=(2,1)',-2.5,color=YELLOW)
        self.play(Write(answer))
        self.play(FadeIn(self.note('Проверка: 2·2 + 1 = 5 и 2 − 1 = 1. Ответ подходит обоим уравнениям.')));self.wait(6)
