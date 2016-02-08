from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.properties import BooleanProperty


class StagePanel(GridLayout):

    down = BooleanProperty(False)

    def __init__(self, stage, group, parent):
        super(StagePanel, self).__init__()
        self.stage = stage
        self.cbxStage = CheckBox(id=str(stage), group=group, size_hint_x=None,
                                width=40, on_release=parent.change_selected)
        self.build()

    def build(self):
        self.add_widget(self.cbxStage)
        self.add_widget(Label(text='Fase ' + str(self.stage)))

    def on_disabled(self, instance, value):
        if value:
            self.cbxStage.state = 'normal'

    def on_down(self, instance, value):
        if value:
            self.cbxStage.state = 'down'
        else:
            self.cbxStage.state = 'normal'