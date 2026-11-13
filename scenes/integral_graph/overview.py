from manim import *
from scenes.integral_graph.common import IntegralBase
import numpy as np
class Overview(IntegralBase):
    def construct(self):
        self.title('Итог: график и вычисленные особенности')
        group=self.summary();self.play(FadeIn(group),run_time=1.2)
        ax=group[0]
        zeros=VGroup(*[Dot(ax.c2p(x,0),color=ORANGE,radius=.055) for x in [-2*np.sqrt(3),2*np.sqrt(3)]])
        self.play(FadeIn(zeros))
        note=self.note('Нули: −2√3, 0, 2√3. Производная ответа и все указанные точки проверены.')
        self.play(FadeIn(note));self.wait(7)
class IntegralGraphSample(IntegralBase):
    def construct(self):
        self.title('Быстрая проверка композиции')
        group=self.summary();self.play(FadeIn(group),run_time=.6)
        self.play(FadeIn(self.note('Проверяем оси, экстремумы, подписи и границы кадра.')),run_time=.4)
        self.wait(2)
