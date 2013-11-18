from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from random import random

class CircleWidget(Widget):
    def __init__(self, color=Color(1., 1., 0.), **kwargs):
        Widget.__init__(self, **kwargs)
        self.size = (50,50)
        self.circle = Ellipse(pos = self.pos, size = self.size)
        self.canvas.add(color)
        self.canvas.add(self.circle)

    # handle position change
    def on_pos(self, obj, new_pos):
        self.circle.pos = new_pos # when widget moves, so does the graphic instruction

class RootWidget(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.cw1 = CircleWidget(Color(1., 0., 1.))
        self.cw2 = CircleWidget(Color(0., 0., 1.))
        self.add_widget(self.cw1)
        self.add_widget(self.cw2)

    def update(self, dt):
        self.cw1.pos = (random()*200, random()*200)
        self.cw2.pos = (random()*200, random()*200)

class MyApp(App):
    def build(self):
        rw = RootWidget()
        # call update() every second
        Clock.schedule_interval(rw.update, 0.1)
        return rw

MyApp().run()
