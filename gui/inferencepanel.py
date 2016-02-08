from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from reader.updater import Updater
from reader.parser import Parser
from idp.idp import IDP
from gui.grouppanel import GroupPanel
from gui.undopopup import UndoPopup
from gui.distributionpopup import DistributionPopup
from gui.propagationpopup import PropagationPopup
from gui.elements import TotalLayout, HistoryLabel


class InferencePanel(BoxLayout):

    def __init__(self, url, panel):
        super(InferencePanel, self).__init__()
        self.history = list()
        self.panel = panel
        self.callback = False
        self.updater = Updater()
        self.parser = Parser()
        self.programme_main = self.parser.read(url)
        self.choices = dict()
        self.programme_init = self.programme_main.clone()
        self.idp = IDP()
        self.pnlProgramme = GroupPanel(self.programme_main, self)
        self.svHistory = ScrollView()
        self.dbOptions = DropDown()
        self.btnSelect = Button(text='Select Term', size_hint_y=None, height=30)
        self.build()
        self.callback = True
        self.update([])

    def build(self):
        bltAll = TotalLayout()
        svMain = ScrollView()
        bltCenter = BoxLayout(orientation='vertical')
        bltBottom = BoxLayout(size_hint_y=None, height=36)
        btnExpand = Button(text='Expand', size_hint_y=None, height=30, on_release=self.expand)
        btnOptimize = Button(text='Optimize', size_hint_y=None, height=30, on_release=self.minimize)
        self.btnSelect.bind(on_release=self.dbOptions.open)
        for name in self.idp.terms.keys():
            btnTerm = Button(text=name, size_hint_y=None, height=30)
            btnTerm.bind(on_release=lambda btnTerm: self.dbOptions.select(btnTerm.text))
            self.dbOptions.add_widget(btnTerm)
        self.dbOptions.bind(on_select=lambda instance, x: setattr(self.btnSelect, 'text', x))
        btnDistri = Button(size_hint_y=None, height=30, text='ECTS Stats', on_release=self.show_distribution_popup)
        bltBottom.add_widget(btnExpand)
        bltBottom.add_widget(btnOptimize)
        bltBottom.add_widget(self.btnSelect)
        bltBottom.add_widget(btnDistri)
        svMain.add_widget(self.pnlProgramme)
        bltCenter.add_widget(svMain)
        bltCenter.add_widget(bltBottom)
        bltAll.add_widget(bltCenter)
        bltRight = BoxLayout(size_hint_x=None, width=200, orientation='vertical', spacing=2)
        bltRight.add_widget(HistoryLabel(text='History'))
        bltRight.add_widget(self.svHistory)
        bltAll.add_widget(bltRight)
        self.add_widget(bltAll)

    def update(self, choices):
        if self.callback:
            s = self.sat(choices)
            if self.idp.sat(self.parser.print_domain(s)):
                self.step(choices)
            else:
                self.show_unsat_popup(s, choices)

    def propagate(self, programme):
        i = self.parser.print_domain(programme)
        self.updater.filter(i)
        self.updater.filter(self.idp.propagate(i))
        self.updater.update_programme(programme)

    def sat(self, choices):
        programme = self.programme_init.clone()
        for course in self.choices.values():
            programme.update_not_interested(course.code, course.not_interested)
            programme.update_selected(course.code, course.selected)
        for course in choices:
            programme.update_not_interested(course.code, course.not_interested)
            programme.update_selected(course.code, course.selected)
        return programme

    def expand(self, *args):
        i = self.parser.print_domain(self.programme_main)
        self.updater.filter(i)
        self.updater.filter(self.idp.expand(i))
        self.updater.update_programme(self.programme_main)
        self.refresh()

    def minimize(self, *args):
        if self.btnSelect.text != 'Select':
            i = self.parser.print_domain(self.programme_main)
            self.updater.filter(i)
            self.updater.filter(self.idp.minimize(self.btnSelect.text, i))
            self.updater.update_programme(self.programme_main)
            self.refresh()

    def refresh(self):
        self.callback = False
        for code in self.choices.keys():
            course = self.choices.get(code)
            if not course.not_interested and course.selected is None:
                self.choices.pop(code)
        self.panel.update(self.programme_main.get_selected_courses())
        self.pnlProgramme.refresh()
        self.callback = True

    def show_unsat_popup(self, programme, choices):
        t = self.updater.get_unsat(self.idp.unsat(self.parser.print_domain(programme)))
        courses = list()
        for code in t:
            courses.append(self.programme_main.get_course(code))
        ppUndo = UndoPopup(courses, choices, self)
        ppUndo.open()

    def show_distribution_popup(self, *args):
        ppDistri = DistributionPopup(self.programme_main.get_ects_distribution(),
                                     self.programme_main.get_min_ects(),
                                     self.programme_main.get_max_ects())
        ppDistri.open()

    def step(self, choices):
        codes = list()
        ch_new = self.choices.copy()
        for course in choices:
            ch_new[course.code] = course
            codes.append(course.code)
        programme = self.sat(choices)
        self.propagate(programme)
        pr_new, un_new = self.split_courses(programme.get_all_courses(), ch_new.keys())
        pr_old, un_old = self.split_courses(self.programme_main.get_all_courses(), ch_new.keys())
        #propagations = list()
        #before = list()
        #for code in pr_new.keys():
        #    if code not in pr_old.keys():
        #        propagations.append(pr_new.get(code))
        #        before.append(un_old.get(code))
        #    elif not pr_new.get(code) == pr_old.get(code):
        #        propagations.append(pr_new.get(code))
        #        before.append(pr_old.get(code))
        unknown = list()
        unknown_before = list()
        for code in pr_old.keys():
            if code in un_new.keys():
                unknown.append(un_new.get(code))
                unknown_before.append(pr_old.get(code))
        if len(unknown) == 0:
            for course in choices:
                self.choices[course.code] = course
            for course in programme.get_all_courses().values():
                self.programme_main.update_not_interested(course.code, course.not_interested)
                self.programme_main.update_selected(course.code, course.selected)
            self.refresh()
        else:
            ppProp = PropagationPopup(choices, unknown, unknown_before, self)
            ppProp.open()

    def split_courses(self, courses, codes):
        propagations = dict()
        unknowns = dict()
        for code in courses.keys():
            if code not in codes:
                course = courses.get(code)
                if course.selected is None and course.not_interested is False:
                    unknowns[code] = course
                else:
                    propagations[code] = course
        return propagations, unknowns
