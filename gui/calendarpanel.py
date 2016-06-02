from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivycalendar import CalendarWidget
from gui.daypanel import DayPanel
from data.schedule import CompleteSchedule
from idp.schedule.idpschedule import IDPSchedule
from reader.roster import Roster
from reader.overlapparser import Parser
from gui.elements import CompleteLayout


class CalendarPanel(BoxLayout):

    def __init__(self, stages, location):
        super(CalendarPanel, self).__init__()
        self.calendar = CalendarWidget()
        self.calendar.bind(active_date=self.change_day)
        self.completeSchedule = CompleteSchedule(stages)
        self.roster = Roster(location + 'reader/',
                             ['msti.txt','mscw.txt','mscs.txt'],
                             'shadowcourses.txt') #TODO: CHANGE
        self.idpSchedule = IDPSchedule()
        self.svDay = ScrollView()
        self.svBottomRight = ScrollView()
        self.parser = Parser()
        self.boxes = list()
        self.stage = 1
        for stage in self.completeSchedule.get_stages():
            self.boxes.append(CheckBox(id=str(stage),
                                       group='stages',
                                       on_release=self.change_stage,
                                       allow_no_selection=False))
        self.build()
        self.change_day()

    def build(self):
        bltComplete = CompleteLayout()
        self.calendar.size_hint = (None, None)
        self.calendar.size = (400, 400)
        self.calendar.pos_hint = {'top': 1}
        bltLeft = BoxLayout(orientation='vertical', size_hint_x=None, width=400, spacing=30)
        bltTopLeft = BoxLayout()
        bltBottomLeft = BoxLayout(orientation='vertical')
        bltBottomLeft.add_widget(Label(text='Fases:', size_hint_y=None, height=30))
        for cbxStage in self.boxes:
            bltStage = BoxLayout(size_hint=(None,None), size=(200,30))
            bltStage.add_widget(Label(text=str(cbxStage.id), size_hint_y=None, height=30))
            bltStage.add_widget(cbxStage)
            bltBottomLeft.add_widget(bltStage)
        bltBottomLeft.add_widget(BoxLayout())
        bltTopLeft.add_widget(self.calendar)
        bltLeft.add_widget(bltTopLeft)
        bltLeft.add_widget(bltBottomLeft)
        bltComplete.add_widget(bltLeft)

        bltRight = BoxLayout(orientation='vertical', spacing=30)
        bltTopRight = BoxLayout(orientation='vertical')
        lblDay = Label(text='Agenda:', size_hint_y=None, height=30)
        bltTopRight.add_widget(lblDay)
        bltTopRight.add_widget(self.svDay)
        bltRight.add_widget(bltTopRight)

        bltBottomRight = BoxLayout(orientation='vertical')
        lblStats = Label(text='Statistieken:', size_hint_y=None, height=30)
        bltBottomRight.add_widget(lblStats)
        bltBottomRight.add_widget(self.svBottomRight)
        btnCalculate = Button(text='bereken overlap', size_hint_y=None, height=30, on_release=self.update)
        bltBottomRight.add_widget(btnCalculate)
        bltRight.add_widget(bltBottomRight)

        bltComplete.add_widget(bltRight)
        self.add_widget(bltComplete)

    def change_stage(self, cbxStage):
        if cbxStage.state == 'down':
            self.stage = int(cbxStage.id)
        self.change_day()

    def change_day(self, *args):
        date = self.calendar.active_date
        classes = list()
        for schedule in self.completeSchedule.get_schedules(self.stage):
            for c in schedule.classes:
                if c.start.year == date[2]:
                    if c.start.month == date[1]:
                        if c.start.day == date[0]:
                            classes.append(c)
        self.svDay.clear_widgets()
        self.svDay.add_widget(DayPanel(classes,date))

    def update_selected_courses(self, courses):
        for code in courses.keys():
            if courses.get(code) is None:
                for stageSchedule in self.completeSchedule.stageSchedules.values():
                    stageSchedule.remove_schedule(code)
            else:
                self.completeSchedule.add_schedule(self.roster.parse_course(code), courses.get(code))

    def update(self, *args):
        self.svBottomRight.clear_widgets()
        bltLayout = BoxLayout(orientation='vertical')
        for lblOverlap in self.calculate_overlap():
            bltLayout.add_widget(lblOverlap)
        self.svBottomRight.add_widget(bltLayout)

    def calculate_overlap(self):
        results = list()
        for stage in self.completeSchedule.stageSchedules.keys():
            lblOverlap1 = Label(size_hint_y=None, height=30)
            o1 = self.parser.parse_total_overlap(self.idpSchedule.expand(self.completeSchedule.print_structure(stage, 1)))
            lblOverlap1.text = 'Fase ' + str(stage) + ' Semester ' + str(1) + ' overlap/week: ' + str(o1*30) + ' min.'
            results.append(lblOverlap1)
            lblOverlap2 = Label(size_hint_y=None, height=30)
            o2 = self.parser.parse_total_overlap(self.idpSchedule.expand(self.completeSchedule.print_structure(stage, 2)))
            lblOverlap2.text = 'Fase ' + str(stage) + ' Semester ' + str(2) + ' overlap/week: ' + str(o2*30) + ' min.'
            results.append(lblOverlap2)
        return results
