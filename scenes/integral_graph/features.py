from manim import *
from scenes.integral_graph.common import IntegralBase,ACCENT
class Features(IntegralBase):
    def construct(self):
        self.title('Точка перегиба и пересечения оси')
        first=self.line(r"F''(x)=2x=0\quad\Longrightarrow\quad x=0",2.15)
        second=self.line(r"x<0:\ F''<0;\qquad x>0:\ F''>0",1.1,34)
        third=self.line(r'F(0)=0\quad\Longrightarrow\quad(0,0)',.1,color=ACCENT)
        self.play(Write(first));self.play(Write(second));self.play(Write(third));self.wait(3)
        zeros=self.line(r'F(x)=\frac{x(x^2-12)}3=0',-1.2,36)
        roots=self.line(r'x=0\quad\vee\quad x^2=12\quad\Longrightarrow\quad x=0,\ \pm2\sqrt3',-2.3,34)
        self.play(Write(zeros));self.play(Write(roots));self.wait(4)
        self.play(FadeIn(self.note('Вторая производная меняет знак в нуле — это действительно перегиб.')));self.wait(3)
