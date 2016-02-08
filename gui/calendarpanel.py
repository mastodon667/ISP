from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivycalendar import CalendarWidget
from kivy.uix.label import Label
from gui.daypanel import DayPanel


class CalendarPanel(BoxLayout):

    def __init__(self, classes):
        super(CalendarPanel, self).__init__()
        self.calendar = CalendarWidget()
        self.calendar.bind(active_date=self.change_day)
        self.classes = classes
        self.selected_courses = list()
        self.svDay = ScrollView()
        self.build()

    def build(self):
        self.calendar.size_hint = (None,None)
        self.calendar.size = (400,400)
        self.calendar.pos_hint = {'top': 1}
        bltLeft = BoxLayout()
        bltLeft.add_widget(self.calendar)
        self.add_widget(bltLeft)

        bltRight = BoxLayout(orientation='vertical')

        bltTopRight = BoxLayout(orientation='vertical')
        lblDay = Label(text='Daily Agenda:', size_hint_y=None, height=30)
        bltTopRight.add_widget(lblDay)
        bltTopRight.add_widget(self.svDay)
        bltRight.add_widget(bltTopRight)

        bltBottomRight = BoxLayout(orientation='vertical')
        lblStats = Label(text='Statistics:', size_hint_y=None, height=30)
        bltBottomRight.add_widget(lblStats)
        bltRight.add_widget(bltBottomRight)

        self.add_widget(bltRight)
        self.change_day()

    def change_day(self, *args):
        date = self.calendar.active_date
        classes = list()
        for code in self.selected_courses:
            for c in self.classes.get(code):
                if c.start.year == date[2]:
                    if c.start.month == date[1]:
                        if c.start.day == date[0]:
                            classes.append(c)
        self.svDay.clear_widgets()
        self.svDay.add_widget(DayPanel(classes))

    def update_selected_courses(self, courses):
        self.selected_courses = courses
