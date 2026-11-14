from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Gauss(SystemsBase):
    def construct(self):
        self.heading('5. Метод Гаусса')
        def matrix(tex):return self.eq(r'\left[\begin{array}{cc|c}'+tex+r'\end{array}\right]',.9,height=2).move_to([-2.7,.9,0])
        current=matrix(r'2&1&5\\1&-1&1')
        self.play(Write(current))
        note=self.note('Записываем коэффициенты и правые части в расширенную матрицу.')
        self.play(FadeIn(note));self.wait(2)
        op=self.eq(r'R_1\leftrightarrow R_2',.9,size=33).move_to([3.4,.9,0])
        next_matrix=matrix(r'1&-1&1\\2&1&5')
        self.play(Write(op),ReplacementTransform(current,next_matrix));current=next_matrix;self.wait(2)
        newop=self.eq(r'R_2\leftarrow R_2-2R_1',.9,size=32).move_to([3.4,.9,0])
        next_matrix=matrix(r'1&-1&1\\0&3&3')
        self.play(ReplacementTransform(op,newop),ReplacementTransform(current,next_matrix));self.wait(2)
        arithmetic=self.eq('(2,1,5)-2(1,-1,1)=(0,3,3)',-1,size=33)
        self.play(Write(arithmetic));self.wait(2)
        back=self.eq(r'3y=3\Rightarrow y=1;\qquad x-y=1\Rightarrow x=1+1=2',-2,size=33,color=ACCENT)
        self.play(Write(back));self.wait(3)
        end=self.note('Прямой ход исключает x из второй строки; обратный ход находит y и x.')
        self.play(ReplacementTransform(note,end));self.wait(3)
