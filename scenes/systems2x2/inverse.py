from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Inverse(SystemsBase):
    def construct(self):
        self.heading('6. Матричный метод: обратная матрица')
        start=self.eq(r'AX=b,\quad A=\begin{pmatrix}2&1\\1&-1\end{pmatrix},\quad X=\begin{pmatrix}x\\y\end{pmatrix},\quad b=\begin{pmatrix}5\\1\end{pmatrix}',2.05,size=33,height=1.35)
        self.play(Write(start));self.wait(2)
        generic=self.eq(r'A^{-1}=\frac1{\det A}\begin{pmatrix}-1&-1\\-1&2\end{pmatrix}',.25,size=35,height=1.35)
        adjugate=self.note('Меняем диагональные элементы местами, у остальных меняем знаки.')
        self.play(Write(generic),FadeIn(adjugate));self.wait(3)
        numeric=self.eq(r'A^{-1}=\frac1{-3}\begin{pmatrix}-1&-1\\-1&2\end{pmatrix}',.25,size=35,height=1.35,color=ACCENT)
        self.play(TransformMatchingTex(generic,numeric));self.wait(2)
        product=self.eq(r'X=A^{-1}b=-\frac13\begin{pmatrix}-5-1\\-5+2\end{pmatrix}=-\frac13\begin{pmatrix}-6\\-3\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}',-1.65,size=33,height=1.35)
        self.play(Write(product));self.wait(4)
        self.play(ReplacementTransform(adjugate,self.note('Обратная матрица существует, поскольку det A = −3 ≠ 0.')));self.wait(3)
