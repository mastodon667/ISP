from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from gui.stagepanel import StagePanel
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty, BooleanProperty
from gui.elements import CourseLabel


class CoursePanel(BoxLayout):

    term = NumericProperty(1)
    selected = NumericProperty(None, allownone=True)
    not_interested = BooleanProperty(False)

    def __init__(self, course, panel):
        super(CoursePanel, self).__init__()
        self.panel = panel
        self.term = course.term
        self.tbtnSelect = ToggleButton(size_hint=(None, None), size=(200, 40),
                                       text='Not Interested', on_release=self.toggle_not_interested)
        self.stagePanels = list()
        self.course = course
        self.build()

    def build(self):
        bltTop = BoxLayout(padding=[10, 10, 10, 0])
        lblName = CourseLabel(text=self.course.name + ' (' + str(self.course.ects) + ')')
        lblCode = Label(text=self.course.code, size_hint_x=None, width=80)
        bltTop.add_widget(lblName)
        bltTop.add_widget(lblCode)
        self.add_widget(bltTop)
        bltBottom = BoxLayout(spacing=10, padding=[10, 0, 10, 10])
        for stage in self.course.stages:
            pnlStage = StagePanel(stage, self.course.code, self)
            self.stagePanels.append(pnlStage)
            bltBottom.add_widget(pnlStage)
        self.add_widget(bltBottom)
        bltBottom.add_widget(self.tbtnSelect)
        self.refresh()

    def toggle_not_interested(self, button):
        self.not_interested = button.state == 'down'

    def change_selected(self, checkbox):
        if checkbox.state == 'normal':
            self.selected = None
        else:
            self.selected = int(checkbox.id)

    def on_not_interested(self, *args):
        self.course.not_interested = self.not_interested
        if self.not_interested:
            self.tbtnSelect.state = 'down'
            for pnlStage in self.stagePanels:
                pnlStage.disabled = self.tbtnSelect.state == 'down'
            if self.selected is None:
                self.on_selected()
            else:
                self.selected = None
        else:
            self.tbtnSelect.state = 'normal'
            for pnlStage in self.stagePanels:
                pnlStage.disabled = self.tbtnSelect.state == 'down'
            if self.panel is not None:
                self.panel.update([self.course.clone()])

    def on_selected(self, *args):
        if self.selected is None:
            self.course.selected = None
        else:
            self.course.selected = int(self.selected)
        for pnlStage in self.stagePanels:
            if pnlStage.stage == self.course.selected:
                pnlStage.down = True
            else:
                pnlStage.down = False
        if self.panel is not None:
            self.panel.update([self.course.clone()])

    def refresh(self):
        self.selected = self.course.selected
        self.not_interested = self.course.not_interested
