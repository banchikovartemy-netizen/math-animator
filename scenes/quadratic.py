from manim import *
import sympy as sp
from animation.components import ExplainedScene
from examples.quadratic_data import A, B, C


class QuadraticEquation(ExplainedScene):
    def construct(self):
        self.camera.background_color = BLACK
        config.tex_template = TexTemplate(
            preamble=r"\usepackage{amsmath}\usepackage{amssymb}"
        )
        a, b, c = [sp.Rational(str(value)) for value in (A, B, C)]
        if a == 0:
            raise ValueError("Коэффициент A должен быть отличен от нуля.")
        x = sp.Symbol("x")
        polynomial = a * x**2 + b * x + c
        discriminant = sp.simplify(b**2 - 4 * a * c)
        root1 = sp.simplify((-b + sp.sqrt(discriminant)) / (2 * a))
        root2 = sp.simplify((-b - sp.sqrt(discriminant)) / (2 * a))
        for root in (root1, root2):
            assert sp.simplify(polynomial.subs(x, root)) == 0
        tex = sp.latex

        def fit(obj, width=12, height=1.2):
            if obj.width > width: obj.scale_to_fit_width(width)
            if obj.height > height: obj.scale_to_fit_height(height)
            return obj

        def formula(expression, y=0, color=WHITE):
            return fit(MathTex(expression, font_size=42, color=color)).move_to(UP * y)

        caption = None

        def explain(message):
            nonlocal caption
            new = fit(Text(message, font="DejaVu Sans", font_size=26),height=0.6).to_edge(DOWN, buff=0.35)
            if caption is None: self.play(FadeIn(new))
            else: self.play(ReplacementTransform(caption, new))
            caption = new
            self.wait(1.5)

        title = fit(Text("Решение квадратного уравнения",font="DejaVu Sans",font_size=34),height=0.6).to_edge(UP, buff=0.3)
        equation = formula(tex(sp.Eq(polynomial, 0, evaluate=False)),y=2.2,color=YELLOW)
        self.play(Write(title), Write(equation))
        explain("Найдём дискриминант, затем вычислим корни.")
        current = formula(r"D=b^2-4ac", y=0.5)
        self.play(Write(current)); self.wait(1)
        substitution = formula(rf"D=({tex(b)})^2-4\cdot({tex(a)})\cdot({tex(c)})={tex(discriminant)}",y=0.5)
        self.play(TransformMatchingTex(current, substitution)); self.wait(2)
        if discriminant > 0: explain("D > 0: два различных действительных корня.")
        elif discriminant == 0: explain("D = 0: один действительный корень кратности два.")
        else: explain("D < 0: действительных корней нет. Найдём комплексные.")
        rule = formula(r"x_{1,2}=\frac{-b\pm\sqrt{D}}{2a}",y=0.5,color=TEAL)
        self.play(ReplacementTransform(substitution, rule)); self.wait(2); self.play(FadeOut(rule))
        if discriminant == 0:
            result = formula(rf"x=\frac{{-({tex(b)})}}{{2\cdot({tex(a)})}}={tex(root1)}",y=0.2,color=TEAL)
            self.play(Write(result)); self.play(Create(SurroundingRectangle(result, color=TEAL)))
        else:
            results = VGroup()
            for index, sign, root, y_position in [(1, "+", root1, 0.7),(2, "-", root2, -1.2)]:
                result = formula(rf"x_{index}=\frac{{-({tex(b)}){sign}\sqrt{{{tex(discriminant)}}}}}{{2\cdot({tex(a)})}}={tex(root)}",y=y_position,color=TEAL)
                self.play(Write(result)); self.wait(2); results.add(result)
            self.play(Create(SurroundingRectangle(results, color=TEAL)))
        explain("Каждый найденный корень проверен подстановкой через SymPy.")
        self.wait(4)
