from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from gui.solutionpanel import SolutionsPanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class UndoPopup(Popup):
    def __init__(self, solutions, choices, all_choices, rules, window):
        super(UndoPopup, self).__init__()
        self.title = 'Undo'
        self.window = window
        self.rules = rules
        self.size_hint = None, None
        self.size = 700, 500
        self.solutions = solutions
        self.choices = dict()
        self.all_choices = all_choices
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

    def get_sol(self):
        for pnlSol in self.panels:
            if pnlSol.cbxSelect.state == 'down':
                return pnlSol.solution

    def in_new_choices(self, code):
        for choice in self.choices:
            if code == choice.code:
                return True
        return False

    def on_dismiss(self):
        sol = self.get_sol()
        for choice in self.all_choices:
            if choice.code in sol:
                if not self.in_new_choices(choice.code):
                    self.choices.append(choice)
        for choice in self.choices:
            if choice.code in sol:
                choice.not_interested = False
                choice.selected = None
        self.window.update(self.choices)
