from manim import *
from scenes.integral_graph.common import IntegralBase,ACCENT
class Critical(IntegralBase):
    def construct(self):
        self.title('Где функция растёт и убывает?')
        f=self.line(r"F'(x)=x^2-4",2.35)
        self.play(Write(f))
        zeros=self.line(r'x^2-4=0\ \Longrightarrow\ (x-2)(x+2)=0',1.25,35)
        roots=self.line(r'x_1=-2,\qquad x_2=2',.25,color=ACCENT)
        self.play(Write(zeros));self.wait(2);self.play(Write(roots))
        axis=NumberLine(x_range=[-4,4,1],length=10,include_numbers=True,font_size=23).move_to(DOWN*1.2)
        signs=VGroup(MathTex('+',color=GREEN).move_to([-4,-.65,0]),MathTex('-',color=RED).move_to([0,-.65,0]),MathTex('+',color=GREEN).move_to([4,-.65,0]))
        marks=VGroup(*[Dot(axis.n2p(v),color=YELLOW) for v in [-2,2]])
        arrows=VGroup(Arrow([-5,-2.35,0],[-3,-1.85,0],color=GREEN),Arrow([-1,-1.85,0],[1,-2.35,0],color=RED),Arrow([3,-2.35,0],[5,-1.85,0],color=GREEN))
        self.play(Create(axis),FadeIn(marks));self.play(Write(signs),Create(arrows))
        note=self.note('F′ > 0: рост; F′ < 0: убывание. В точках ±2 производная равна нулю.')
        self.play(FadeIn(note));self.wait(5)
