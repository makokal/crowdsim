from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from random import random

class CircleWidget(Widget):
    def __init__(self, color=Color(1., 1., 0.), size=(50, 50), pos=(100, 100), **kwargs):
        Widget.__init__(self, **kwargs)
        self.size = size
        self.pos = pos
        self.ball = Ellipse(pos = self.pos, size = self.size)
        self.canvas.add(color)
        self.canvas.add(self.ball)

    # handle position change
    def on_pos(self, obj, new_pos):
        self.ball.pos = new_pos # when widget moves, so does the graphic instruction

class RootWidget(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.balls = []
        for i in xrange(5):
            self.balls.append( CircleWidget(color=Color(1-i, 0., i), pos=(i*100, i*100)) )

        for ball in self.balls:
            self.add_widget(ball)

    def update(self, dt):
        for ball in self.balls:
            ball.pos = (random()*200, random()*200)

class MyApp(App):
    def build(self):
        rw = RootWidget()
        # call update() every second
        Clock.schedule_interval(rw.update, 0.1)
        return rw

MyApp().run()
