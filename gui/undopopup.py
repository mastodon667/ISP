from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from gui.solutionpanel import SolutionsPanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class UndoPopup(Popup):
    def __init__(self, solutions, choices, rules, window):
        super(UndoPopup, self).__init__()
        self.title = 'Undo'
        self.window = window
        self.rules = rules
        self.size_hint = None, None
        self.size = 700, 500
        self.solutions = solutions
        self.choices = dict()
        self.choices = choices
        self.panels = list()
        self.build()

    def build(self):
        svMain = ScrollView()
        bltSolutions = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        h = -10
        i = 1
        for solution in self.solutions:
            pnlSol = SolutionsPanel(solution, i, 'sol')
            h += pnlSol.height+10
            bltSolutions.add_widget(pnlSol)
            self.panels.append(pnlSol)
            i += 1
        bltSolutions.height = h
        bltRules = BoxLayout(size_hint_y=None, height=50)
        bltRules.add_widget(Label(text=self.rules))
        bltTotal = BoxLayout(orientation='vertical', size_hint_y=None, height=h+50)
        bltTotal.add_widget(bltSolutions)
        bltTotal.add_widget(bltRules)
        svMain.add_widget(bltTotal)
        self.add_widget(svMain)

    def on_dismiss(self):
        for course in self.courses:
            c = self.backup.get(course.code)
            if (course.selected != c.selected) or (course.not_interested != c.not_interested):
                self.choices[course.code] = course
        self.window.update(self.choices.values())
