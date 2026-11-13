from manim import *
from scenes.integral_graph.common import IntegralBase,ACCENT
class Integrate(IntegralBase):
    def construct(self):
        self.title('Сначала вычислим интеграл')
        eq=self.line(r'\int(x^2-4)\,dx',1.4)
        self.play(Write(eq));self.wait(1.5)
        next_eq=self.line(r'\int x^2\,dx-4\int1\,dx',1.4)
        self.play(TransformMatchingTex(eq,next_eq));eq=next_eq
        note=self.note('Интегрируем каждое слагаемое: степень увеличиваем на 1.')
        self.play(FadeIn(note))
        rule=self.line(r'\int x^n dx=\frac{x^{n+1}}{n+1}+C\quad(n\ne-1)',-.15,33)
        self.play(Write(rule));self.wait(3)
        answer=self.line(r'\int(x^2-4)\,dx=\frac{x^3}{3}-4x+C',1.4,color=ACCENT)
        self.play(ReplacementTransform(eq,answer),FadeOut(rule))
        check=self.line(r'\frac{d}{dx}\left(\frac{x^3}{3}-4x+C\right)=x^2-4',-.25,35)
        self.play(Write(check));self.wait(3)
        graph=self.line(r'F(x)=\frac{x^3}{3}-4x\quad(C=0)',-1.7,35)
        self.play(Write(graph),FadeOut(note))
        caption=self.note('Далее строим график при C = 0; другие C сдвигают его по вертикали.')
        self.play(FadeIn(caption));self.wait(3)
