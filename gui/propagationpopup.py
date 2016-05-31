from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox


class PropagationPopup(Popup):

    def __init__(self, choices, courses, before, window):
        super(PropagationPopup, self).__init__()
        self.before = before
        self.choices = choices
        self.courses = courses
        self.title = 'Wil je de propagaties behouden?'
        self.window = window
        self.size_hint = None, None
        self.size = 700, 500
        self.boxes = list()
        self.build()

    def build(self):
        svMain = ScrollView()
        h = len(self.courses)*30
        bltMain = BoxLayout(orientation='vertical', size_hint_y=None, height=h)
        for course in self.courses:
            bltItem = BoxLayout(size_hint_y=None, height=30, orientation='vertical')
            bltTop = BoxLayout(size_hint_y=None, height=15)
            bltBottom = BoxLayout(size_hint_y=None, height=15)
            bltTop.add_widget(Label(text=str(course), size_hint_y=None, height=15))
            bltBottom.add_widget(Label(text=str(self.get_before(course.code)), size_hint_y=None, height=15))
            cbxItem = CheckBox(id=course.code)
            self.boxes.append(cbxItem)
            bltBottom.add_widget(cbxItem)
            bltItem.add_widget(bltTop)
            bltItem.add_widget(bltBottom)
            bltMain.add_widget(bltItem)
        svMain.add_widget(bltMain)
        self.add_widget(svMain)

    def get_before(self, code):
        for course in self.before:
            if course.code == code:
                return course
        return None

    def get_after(self, code):
        for course in self.courses:
            if course.code == code:
                return course
        return None

    def on_dismiss(self):
        for checkbox in self.boxes:
            if checkbox.state == 'down':
                self.choices.append(self.get_before(checkbox.id))
            else:
                self.choices.append(self.get_after(checkbox.id))
        self.window.update(self.choices)