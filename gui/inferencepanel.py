from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from reader.updater import Updater
from reader.parser import Parser
from idp.idp import IDP
from data.action import UserAction, InferenceAction
from gui.grouppanel import GroupPanel
from gui.undopopup import UndoPopup
from gui.distributionpopup import DistributionPopup
from gui.propagationpopup import PropagationPopup
from gui.undoactionpopup import UndoActionPopup
from gui.elements import TotalLayout, HistoryLabel, ActLabel


class InferencePanel(BoxLayout):

    def __init__(self, url, panel):
        super(InferencePanel, self).__init__()
        self.history = list()
        self.panel = panel
        self.callback = False
        self.updater = Updater()
        self.parser = Parser()
        self.programme_main = self.parser.read(url)
        self.programme_temp = self.programme_main.clone()
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
        bltRight.add_widget(Button(text='Undo', size_hint_y=None, height=30, on_release=self.show_undo_action_popup))
        bltAll.add_widget(bltRight)
        self.add_widget(bltAll)

    def update(self, choices):
        if self.callback:
            s = self.sat(choices)
            if self.idp.sat(self.parser.print_domain(s)):
                self.blahblah(choices)
            else:
                self.show_unsat_popup(s, choices)

    def propagate(self, programme):
        i = self.parser.print_domain(programme)
        self.updater.filter(i)
        self.updater.filter(self.idp.propagate(i))
        self.updater.update_programme(programme)

    def sat(self, choices):
        programme = self.programme_init.clone()
        for action in self.history:
            if isinstance(action, UserAction):
                for course in action.choices:
                    programme.update_not_interested(course.code, course.not_interested)
                    programme.update_selected(course.code, course.selected)
            elif isinstance(action, InferenceAction):
                for course in action.after:
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
        self.create_inference_action('Model Expansion')
        self.refresh()

    def minimize(self, *args):
        if self.btnSelect.text != 'Select':
            i = self.parser.print_domain(self.programme_main)
            self.updater.filter(i)
            self.updater.filter(self.idp.minimize(self.btnSelect.text, i))
            self.updater.update_programme(self.programme_main)
            self.create_inference_action('Minimization: ' + self.btnSelect.text)
            self.refresh()

    def refresh(self):
        self.callback = False
        self.panel.update(self.programme_main.get_selected_courses())
        self.pnlProgramme.refresh()
        self.callback = True

    def create_user_action(self, choices, propagations, before):
        if len(before) > 0:
            self.history.append(UserAction(choices, propagations, before))
            self.update_history()
        for course in choices:
            self.programme_main.update_not_interested(course.code, course.not_interested)
            self.programme_main.update_selected(course.code, course.selected)
        for course in propagations:
            self.programme_main.update_not_interested(course.code, course.not_interested)
            self.programme_main.update_selected(course.code, course.selected)
        self.programme_temp = self.programme_main.clone()

    def create_inference_action(self, inference):
        new = self.programme_main.get_all_vakken()
        old = self.programme_temp.get_all_vakken()
        before = list()
        after = list()
        for code in new.keys():
            course_new = new.get(code)
            course_old = old.get(code)
            if (course_new.selected != course_old.selected) or \
                    (course_new.not_interested != course_old.not_interested):
                before.append(course_old)
                after.append(course_new)
        self.history.append(InferenceAction(inference, after, before))
        self.programme_temp = self.programme_main.clone()
        self.update_history()

    def update_history(self):
        self.svHistory.clear_widgets()
        bltHistory = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None, height=32*len(self.history) - 2)
        for action in self.history:
            bltHistory.add_widget(ActLabel(text=str(action)))
        self.svHistory.add_widget(bltHistory)

    def show_undo_action_popup(self, *args):
        if len(self.history) > 0:
            action = self.history[len(self.history)-1]
            if isinstance(action, UserAction) and len(action.propagations) > 0:
                ppUndoAction = UndoActionPopup(action, self)
                ppUndoAction.open()
            else:
                self.undo_action(action.before)

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

    def undo_action(self, courses):
        if len(self.history) > 0:
            self.history.pop(len(self.history)-1)
            for course in courses:
                self.programme_main.update_not_interested(course.code, course.not_interested)
                self.programme_main.update_selected(course.code, course.selected)
            self.refresh()
            self.update_history()

    def blahblah(self, choices):
        codes = list()
        for course in choices:
            print('User choice: ' + str(course))
            codes.append(course.code)
        ch_old = self.get_all_user_selections([])
        for course in ch_old.values():
            print('User choice (n-1): ' + str(course))
        ch_new = self.get_all_user_selections(choices)
        for course in ch_new.values():
            print('User choice (n): ' + str(course))
        programme = self.programme_init.clone()
        for choice in ch_new.values():
            programme.update_not_interested(choice.code, choice.not_interested)
            programme.update_selected(choice.code, choice.selected)
        self.propagate(programme)
        pr_new, un_new = self.split_courses(programme.get_all_courses(), ch_new.keys())
        pr_old, un_old = self.split_courses(self.programme_temp.get_all_courses(), ch_new.keys())
        for course in pr_old.values():
            print('Old propagation: ' + str(course))
        for course in un_old.values():
            print('Old unknowns: ' + str(course))
        for course in pr_new.values():
            print('New propagation: ' + str(course))
        for course in un_new.values():
            print('New unknowns: ' + str(course))
        #LOOK FOR ANY NEW PROPAGATIONS (=different than previous prop. or previously unknown)
        propagations = list()
        before = list()
        for code in pr_new.keys():
            if code not in pr_old.keys():
                propagations.append(pr_new.get(code))
                before.append(un_old.get(code))
            elif not pr_new.get(code) == pr_old.get(code):
                propagations.append(pr_new.get(code))
                before.append(pr_old.get(code))
        #LOOK FOR VALUES THAT ARE NO LONGER PROPAGATED (where to put them?)
        unknown = list()
        unknown_before = list()
        for code in pr_old.keys():
            if code in un_new.keys():
                unknown.append(un_new.get(code))
                unknown_before.append(pr_old.get(code))
        #IF NO UNDONE PROPAGATIONS, FINISH ACTION AND STORE IT
        if len(unknown) == 0:
            for course in choices:
                before.append(self.programme_temp.get_course(course.code).clone())
            self.create_user_action(choices, propagations, before)
            self.refresh()
        else:
            ppProp = PropagationPopup(choices, unknown, unknown_before, self)
            ppProp.open()
            #SHOW POPUP ASKING USER WHICH OF THE FORMER PROPAGATIONS TO KEEP
            #OUTCOME OF SELECTION TOGETHER WITH CURRENT SELECTION BECOME NEW CHOICES

    def get_all_user_selections(self, choices):
        result = dict()
        for action in self.history:
            if isinstance(action, UserAction):
                for course in action.choices:
                    result[course.code] = course
        for course in choices:
            result[course.code] = course
        return result

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