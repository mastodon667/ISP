from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

class SolutionsPanel(BoxLayout):

    def __init__(self, solution, index, group):
        self.size_hint_y = None
        self.height = 20*(len(solution)+1)
        self.index = index
        self.solution = solution
        self.cbxSelect = CheckBox(id=str(index), group=group, size_hint_x=None,
                                width=40)

    def build(self):
        bltSide = BoxLayout()
        bltMain = BoxLayout(orientation='vertical')
        bltMain.add_widget(Label(text='Solution ' + str(self.index)))
        for code in solution:
            if solution[code] == 0:
                bltMain.add_widget(Label(text=code + ' - Geen interesse'))
            else:
                bltMain.add_widget(Label(text=code + ' - ' + str(solution[code])))
        bltSide.add_widget(self.cbxSelect)
        self.add_widget(bltMain)
        self.add_widget(bltSide)