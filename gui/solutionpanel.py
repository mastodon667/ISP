from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

class SolutionsPanel(BoxLayout):

    def __init__(self, solution, index, group):
        super(SolutionsPanel, self).__init__()
        self.size_hint_y = None
        self.height = 20*(len(solution)+1)
        self.index = index
        self.solution = solution
        self.cbxSelect = CheckBox(id=str(index), group=group, size_hint_x=None, width=40)
        self.build()

    def build(self):
        bltSide = BoxLayout()
        bltMain = BoxLayout(orientation='vertical')
        bltMain.add_widget(Label(text='Solution ' + str(self.index)))
        for code in self.solution:
            if self.solution[code] == '0':
                bltMain.add_widget(Label(text=code + ' - Geen interesse'))
            else:
                bltMain.add_widget(Label(text=code + ' - ' + str(self.solution[code])))
        bltSide.add_widget(self.cbxSelect)
        self.add_widget(bltMain)
        self.add_widget(bltSide)