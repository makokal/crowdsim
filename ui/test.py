from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.clock import Clock
from random import random

class CircleWidget(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.size = (50,50)
        self.circle = Ellipse(pos = self.pos, size = self.size)
        self.canvas.add(self.circle)

    # handle position change
    def on_pos(self, obj, new_pos):
        self.circle.pos = new_pos # when widget moves, so does the graphic instruction

class RootWidget(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.cw = CircleWidget()
        self.add_widget(self.cw)

    def update(self, dt):
        self.cw.pos = (random()*200, random()*200)

class MyApp(App):
    def build(self):
        rw = RootWidget()
        # call update() every second
        Clock.schedule_interval(rw.update, 1.0)
        return rw

MyApp().run()
