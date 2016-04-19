from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from gui.coursepanel import CoursePanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class UndoPopup(Popup):
    def __init__(self, courses, choices, rules, window):
        super(UndoPopup, self).__init__()
        self.title = 'Undo'
        self.window = window
        self.rules = rules
        self.size_hint = None, None
        self.size = 700, 500
        self.courses = courses
        self.choices = dict()
        for course in choices:
            self.choices[course.code] = course
        self.backup = dict()
        for course in courses:
            self.backup[course.code] = course.clone()
        self.panels = list()
        for course in self.courses:
            self.panels.append(CoursePanel(course, None))
        self.build()

    def build(self):
        svMain = ScrollView()
        bltCourses = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None,
                              height=90 * len(self.courses) + 10 * (len(self.courses) - 1))
        for pnlCourse in self.panels:
            bltCourses.add_widget(pnlCourse)
        bltRules = BoxLayout()
        bltRules.add_widget(Label(text=self.rules))
        bltTotal = BoxLayout(orientation='vertical')
        bltTotal.add_widget(bltCourses)
        bltTotal.add_widget(bltRules)
        svMain.add_widget(bltTotal)
        self.add_widget(svMain)

    def on_dismiss(self):
        for course in self.courses:
            c = self.backup.get(course.code)
            if (course.selected != c.selected) or (course.not_interested != c.not_interested):
                self.choices[course.code] = course
        self.window.update(self.choices.values())
