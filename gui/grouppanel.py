from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from gui.coursepanel import CoursePanel
from gui.elements import GroupLabel, TypeLabel


class GroupPanel(GridLayout):
    def __init__(self, group, panel):
        super(GroupPanel, self).__init__()
        self.panel = panel
        self.group = group
        self.coursePanels = list()
        self.groupPanels = list()
        self.build()

    def build(self):
        count = 20
        lblName = GroupLabel(text=self.group.name)
        self.add_widget(lblName)
        count += lblName.height + self.spacing[1]
        if len(self.group.mandatory_courses) > 0:
            lblMandatory = TypeLabel(text='Verplicht')
            self.add_widget(lblMandatory)
            count += lblMandatory.height + self.spacing[1]
            bltMandatory = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
            mcount = 0
            for course in self.group.mandatory_courses:
                pnlCourse = CoursePanel(course, self)
                self.coursePanels.append(pnlCourse)
                bltMandatory.add_widget(pnlCourse)
                mcount += pnlCourse.height
            mcount += bltMandatory.spacing * (len(self.group.mandatory_courses) - 1)
            count += mcount + self.spacing[1]
            bltMandatory.height = mcount
            self.add_widget(bltMandatory)

        if len(self.group.optional_courses) > 0:
            lblOptional = TypeLabel(text='Keuze')
            self.add_widget(lblOptional)
            count += lblOptional.height + self.spacing[1]
            bltOptional = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
            ocount = 0
            for course in self.group.optional_courses:
                pnlCourse = CoursePanel(course, self)
                self.coursePanels.append(pnlCourse)
                bltOptional.add_widget(pnlCourse)
                ocount += pnlCourse.height
            ocount += bltOptional.spacing * (len(self.group.optional_courses) - 1)
            count += ocount + self.spacing[1]
            bltOptional.height = ocount
            self.add_widget(bltOptional)

        for group in self.group.groups:
            #TODO: IF GROUP IS EMPTY DON'T CREATE PANEL
            pnlGroup = GroupPanel(group, self)
            self.groupPanels.append(pnlGroup)
            self.add_widget(pnlGroup)
            count += pnlGroup.height
        count += self.spacing[1] * (len(self.group.groups) - 1)
        self.height = count

    def update(self, course):
        self.panel.update(course)

    def refresh(self):
        for pnlCourse in self.coursePanels:
            pnlCourse.refresh()
        for pnlGroup in self.groupPanels:
            pnlGroup.refresh()
