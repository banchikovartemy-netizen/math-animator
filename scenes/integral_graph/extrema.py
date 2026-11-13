from manim import *
from scenes.integral_graph.common import IntegralBase,ACCENT
class Extrema(IntegralBase):
    def construct(self):
        self.title('Вычислим максимум и минимум')
        lines=[self.line(r"F''(x)=2x",2.5,35),
               self.line(r"F''(-2)=-4<0\quad\Rightarrow\quad\text{local maximum}",1.45,32,YELLOW),
               self.line(r'F(-2)=\frac{(-2)^3}{3}-4(-2)=-\frac83+8=\frac{16}{3}',.4,34,YELLOW),
               self.line(r"F''(2)=4>0\quad\Rightarrow\quad\text{local minimum}",-1,32,BLUE),
               self.line(r'F(2)=\frac{2^3}{3}-4\cdot2=\frac83-8=-\frac{16}{3}',-2.05,34,BLUE)]
        # Explanatory prose is Russian; the coordinate calculations remain LaTeX.
        lines[1]=self.line(r"F''(-2)=-4<0",1.45,35,YELLOW)
        lines[3]=self.line(r"F''(2)=4>0",-1,35,BLUE)
        max_label=self.note('Отрицательная вторая производная: локальный максимум.',y=1.95,size=20)
        min_label=self.note('Положительная вторая производная: локальный минимум.',y=-.5,size=20)
        self.play(Write(lines[0]));self.play(Write(lines[1]),FadeIn(max_label));self.play(Write(lines[2]));self.wait(4)
        self.play(Write(lines[3]),FadeIn(min_label));self.play(Write(lines[4]));self.wait(4)
        self.play(FadeIn(self.note('Экстремумы локальные: кубическая функция не ограничена на всей ℝ.')));self.wait(3)
