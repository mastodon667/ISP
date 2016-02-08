from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from datetime import *


class DayPanel(FloatLayout):

    def __init__(self, classes):
        super(DayPanel, self).__init__()
        self.classes = classes
        self.colors = list()
        self.size_hint_y = None
        self.height = 700
        self.build()

    def build(self):
        with self.canvas:
            for y in range(0,15):
                Color(1,1,1,1)
                Line(points=(self.x,self.y+(self.height/14)*y,self.x+400,self.y+(self.height/14)*y))
            for c in self.classes:
                Color(1,0,0,.5)
                self.create_block(c)
            for c in self.classes:
                Color(1,1,1,1)
                self.create_rectangle(c)

    def create_block(self, c):
        end = datetime(year=c.start.year, month=c.start.month, day=c.start.day, hour=21)
        t = end - c.end
        offset = t.total_seconds()/3600
        w = 100
        h = (self.height/14)*c.get_duration()
        x = self.x
        y = self.y + (self.height/14)*offset
        return Rectangle(pos=(x,y), size=(w,h))

    def create_rectangle(self, c):
        end = datetime(year=c.start.year, month=c.start.month, day=c.start.day, hour=21)
        t = end - c.end
        offset = t.total_seconds()/3600
        w = 100
        h = (self.height/14)*c.get_duration()
        x = self.x
        y = self.y + (self.height/14)*offset
        return Line(rectangle=(x,y,w,h))
