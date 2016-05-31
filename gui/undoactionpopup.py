from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox


class UndoActionPopup(Popup):

    def __init__(self, action, window):
        super(UndoActionPopup, self).__init__()
        self.action = action
        self.title = 'Undo Action'
        self.window = window
        self.size_hint = None, None
        self.size = 700, 500
        self.boxes = list()
        self.build()

    def build(self):
        svMain = ScrollView()
        h = 60+len(self.action.choices)*30 + len(self.action.get_propagations())*30
        bltMain = BoxLayout(orientation='vertical', size_hint_y=None, height=h)
        bltMain.add_widget(Label(text='Keuze gebruiker:', size_hint_y=None, height=30))
        for course in self.action.choices:
            bltMain.add_widget(Label(text=str(course), size_hint_y=None, height=30))
        bltMain.add_widget(Label(text='Propagaties:', size_hint_y=None, height=30))
        propagations = self.action.get_propagations()
        for course in propagations:
            bltItem = BoxLayout(size_hint_y=None, height=30)
            bltItem.add_widget(Label(text=str(course), size_hint_y=None, height=30))
            cbxItem = CheckBox(id=course.code)
            self.boxes.append(cbxItem)
            bltItem.add_widget(cbxItem)
            bltMain.add_widget(bltItem)
        svMain.add_widget(bltMain)
        self.add_widget(svMain)

    def on_dismiss(self):
        courses = list()
        for box in self.boxes:
            if box.state == 'down':
                for course in self.action.get_propagations():
                    if course.code == box.id:
                        courses.append(course)
        self.window.update(courses)
