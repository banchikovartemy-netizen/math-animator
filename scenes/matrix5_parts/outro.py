from manim import *
from animation.components import ExplainedScene,ACCENT
from examples.matrix5_solution import EXPECTED
class Outro(ExplainedScene):
    def construct(self):
        self.heading('Умножение матриц 5 × 5: результат')
        matrix=Matrix(EXPECTED,element_to_mobject_config={'font_size':38},h_buff=1.15,v_buff=.7)
        matrix.scale_to_fit_height(3.6).move_to(UP*.35)
        label=MathTex('C=AB',font_size=39,color=ACCENT).move_to(UP*2.65)
        self.play(FadeIn(matrix),Write(label))
        a=Text('Все 25 элементов проверены независимо через SymPy.',font='DejaVu Sans',font_size=25).move_to(DOWN*2.2)
        b=Text('Вычислено: 125 произведений и 100 сложений.',font='DejaVu Sans',font_size=25).move_to(DOWN*2.85)
        self.check_frame(matrix,label,a,b);self.play(FadeIn(a),FadeIn(b));self.wait(7)
