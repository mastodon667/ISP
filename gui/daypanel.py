from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from datetime import *
from gui.elements import TimeLabel


class DayPanel(FloatLayout):

    def __init__(self, classes, date):
        super(DayPanel, self).__init__()
        self.classes = classes
        self.colors = list()
        self.size_hint_y = None
        self.height = 700
        self.date = datetime(year=date[2],month=date[1],day=date[0],hour=8)
        self.build()

    def build(self):
        for y in range(0,15):
            self.add_widget(TimeLabel(text=str(self.date.hour)+':'+str(self.date.minute), pos_hint={'right': .55}, y=self.y-self.height/2+(self.height/14)*y))
            self.date = self.date + timedelta(hours=1)
        with self.canvas:
            for y in range(0,15):
                Color(1,1,1,1)
                Line(points=(self.x+100,self.y+(self.height/14)*y,self.x+500,self.y+(self.height/14)*y))
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
        x = self.x+200
        y = self.y + (self.height/14)*offset
        return Rectangle(pos=(x,y), size=(w,h))

    def create_rectangle(self, c):
        end = datetime(year=c.start.year, month=c.start.month, day=c.start.day, hour=21)
        t = end - c.end
        offset = t.total_seconds()/3600
        w = 100
        h = (self.height/14)*c.get_duration()
        x = self.x+200
        y = self.y + (self.height/14)*offset
        return Line(rectangle=(x,y,w,h))
