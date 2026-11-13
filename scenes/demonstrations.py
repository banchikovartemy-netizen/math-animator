from manim import *
from animation.components import ExplainedScene, ACCENT
import numpy as np

class Integration(ExplainedScene):
    def construct(self):
        self.heading("Интегрирование по частям")
        eq = self.formula(r"{{\int x e^x\,dx}}", 1.4)
        self.play(Write(eq))
        self.explain("Выбираем множители: производная x становится проще")
        choice = self.formula(r"u=x,\quad dv=e^x dx\quad\Rightarrow\quad du=dx,\quad v=e^x", .1)
        self.play(Write(choice))
        self.explain("Переносим производную на x по формуле интегрирования по частям")
        rule = self.formula(r"\int u\,dv=uv-\int v\,du", -1.25, ACCENT)
        self.play(Write(rule))
        self.wait(1)
        self.play(FadeOut(choice), FadeOut(rule))
        eq = self.transform_formula(eq, r"{{\int x e^x\,dx}}=xe^x-\int e^x\,dx", .7)
        self.explain("Оставшийся интеграл равен экспоненте")
        eq = self.transform_formula(eq, r"{{\int x e^x\,dx}}=e^x(x-1)+C", .7)
        box = SurroundingRectangle(eq, color=ACCENT)
        self.play(Create(box))
        self.explain("Проверка: производная ответа возвращает исходный множитель")
        check = self.formula(r"\frac{d}{dx}\left[e^x(x-1)\right]=e^x(x-1)+e^x=xe^x", -1.1)
        self.play(Write(check))
        self.wait(2)

class Derivative(ExplainedScene):
    def construct(self):
        self.heading("Производная и поведение функции")
        axes = Axes(x_range=[-2.2,2.3,1], y_range=[-3,4,1], x_length=7, y_length=4.5).shift(LEFT*2.3)
        axes.add_coordinates(font_size=20)
        axis_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.check_frame(axis_labels)
        graph = axes.plot(lambda x:x**3-3*x, x_range=[-2.1,2.1], color=BLUE)
        derivative = axes.plot(lambda x:3*x*x-3, x_range=[-1.5,1.5], color=ACCENT)
        self.check_frame(axes, graph, derivative)
        self.play(Create(axes), Write(axis_labels), Create(graph))
        f = self.formula(r"f(x)=x^3-3x").scale(.7).move_to(RIGHT*4+UP*1.5)
        d = self.formula(r"f'(x)=3x^2-3", color=ACCENT).scale(.7).move_to(RIGHT*4+UP*.5)
        self.play(Write(f), Write(d), Create(derivative))
        self.explain("Бирюзовая кривая — производная; её нули дают критические точки")
        dots = VGroup(*[Dot(axes.c2p(x,x**3-3*x), color=YELLOW) for x in (-1,1)])
        self.play(FadeIn(dots))
        tracker = ValueTracker(-1.8)
        moving = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value()**3-3*tracker.get_value()), color=YELLOW))
        tangent = always_redraw(lambda: Line(axes.c2p(tracker.get_value()-.25, tracker.get_value()**3-3*tracker.get_value()-.25*(3*tracker.get_value()**2-3)), axes.c2p(tracker.get_value()+.25, tracker.get_value()**3-3*tracker.get_value()+.25*(3*tracker.get_value()**2-3)), color=YELLOW))
        self.add(moving,tangent)
        self.play(tracker.animate.set_value(1.8),run_time=4)
        self.explain("При x = −1 максимум 2; при x = 1 минимум −2")
        self.wait(2)

class Geometry(ExplainedScene):
    def construct(self):
        self.heading("Прямоугольный треугольник: построение и площадь")
        a,b,c = np.array([-3,-1.5,0]),np.array([1,-1.5,0]),np.array([-3,1.5,0])
        triangle = Polygon(a,b,c,color=BLUE)
        right = RightAngle(Line(a,b),Line(a,c),length=.25)
        labels = VGroup(MathTex("4").next_to(Line(a,b),DOWN),MathTex("3").next_to(Line(a,c),LEFT),MathTex("c").move_to((b+c)/2+UP*.3))
        self.check_frame(triangle,right,labels)
        self.play(Create(triangle),Create(right),Write(labels))
        self.explain("Катеты 3 и 4 перпендикулярны: применяем теорему Пифагора")
        eq = self.formula(r"c^2=3^2+4^2=25", 1).scale(.8).move_to(RIGHT*3.5+UP)
        self.play(Write(eq))
        eq2 = self.formula(r"c=5\quad(c>0)").scale(.8).move_to(RIGHT*3.5)
        self.play(TransformMatchingTex(eq,eq2))
        self.explain("Достраиваем прямоугольник: треугольник занимает ровно половину")
        other = Polygon(b,c,b+c-a,color=ACCENT,fill_opacity=.15)
        self.play(Create(other))
        area=self.formula(r"S=\frac12\cdot3\cdot4=6",-1.4).scale(.8).move_to(RIGHT*3.5+DOWN*1.4)
        self.play(Write(area))
        self.wait(2)

class MatrixProduct(ExplainedScene):
    def construct(self):
        self.heading("Умножение матриц: строка на столбец")
        a=Matrix([[1,2],[3,4]]).scale(.8).move_to(LEFT*4)
        b=Matrix([[2,0],[1,3]]).scale(.8).move_to(LEFT*.8)
        result=Matrix([[4,6],[10,12]]).scale(.8).move_to(RIGHT*3.8)
        symbols=VGroup(MathTex(r"\times").move_to(LEFT*2.4), MathTex("=").move_to(RIGHT*1.5))
        self.check_frame(a,b,result,symbols)
        self.play(Write(a),Write(b),Write(symbols))
        self.explain("Каждая ячейка — скалярное произведение строки и столбца")
        self.play(Write(result.get_brackets()))
        calculation=None
        for i,j,tex in [(0,0,"1\\cdot2+2\\cdot1=4"),(0,1,"1\\cdot0+2\\cdot3=6"),(1,0,"3\\cdot2+4\\cdot1=10"),(1,1,"3\\cdot0+4\\cdot3=12")]:
            row=SurroundingRectangle(a.get_rows()[i],color=YELLOW,buff=.12)
            col=SurroundingRectangle(b.get_columns()[j],color=ACCENT,buff=.12)
            self.play(Create(row),Create(col))
            new=self.formula(tex,-2)
            if calculation is None:self.play(Write(new))
            else:self.play(TransformMatchingTex(calculation,new))
            calculation=new
            self.play(Write(result.get_entries()[2*i+j]))
            self.wait(.8)
            self.play(FadeOut(row),FadeOut(col))
        self.explain("Все четыре элемента вычислены; порядок матриц имеет значение")
        self.wait(2)

class GraphTraversal(ExplainedScene):
    def construct(self):
        self.heading("Поиск кратчайшего пути в невзвешенном графе")
        edges=[(1,2),(1,3),(2,4),(3,4),(4,5)]
        layout={1:LEFT*4,2:LEFT*2+UP*1.5,3:LEFT*2+DOWN*1.5,4:RIGHT*.5,5:RIGHT*3.5}
        graph=Graph([1,2,3,4,5],edges,layout=layout,labels=False,vertex_config={"radius":.28},edge_config={"stroke_width":3})
        numbers = VGroup(*[Text(str(v), font="DejaVu Sans", font_size=24, color="#101827").move_to(graph[v]) for v in graph.vertices])
        self.check_frame(graph, numbers)
        self.play(Create(graph), FadeIn(numbers))
        self.explain("Обход в ширину раскрывает вершины слоями от вершины 1")
        for layer in ([1],[2,3],[4],[5]):
            self.play(*[graph[v].animate.set_color(ACCENT) for v in layer])
            self.wait(.7)
        self.explain("До вершины 5 нужно три ребра: 1 → 2 → 4 → 5")
        self.play(*[graph.edges[e].animate.set_color(YELLOW) for e in [(1,2),(2,4),(4,5)]])
        eq=self.formula(r"d(1,5)=3",-2.2)
        self.play(Write(eq))
        self.wait(2)
