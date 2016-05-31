from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from reader.updater import Updater
from reader.parser import Parser
from reader.explanationparser import ExplanationParser
from idp.explanation.idpexplanation import IDPExplanation
from idp.isp.idpisp import IDPISP
from data.action import UserAction, InferenceAction
from gui.grouppanel import GroupPanel
from gui.undopopup import UndoPopup
from gui.distributionpopup import DistributionPopup
from gui.propagationpopup import PropagationPopup
from gui.undoactionpopup import UndoActionPopup
from gui.elements import TotalLayout, HistoryLabel, ActLabel
from automaton.reader import Reader
import copy


class InferencePanel(BoxLayout):

    def __init__(self, url, panel):
        super(InferencePanel, self).__init__()
        self.history = list()
        r = Reader()
        self.automaton = r.getAutomaton()
        self.panel = panel
        self.callback = False
        self.updater = Updater()
        self.parser = Parser()
        self.explanationParser = ExplanationParser()
        self.programme_main = self.parser.read(url)
        self.programme_temp = self.programme_main.clone()
        self.programme_init = self.programme_main.clone()
        self.idp = IDPISP()
        self.explanation = IDPExplanation()
        self.pnlProgramme = GroupPanel(self.programme_main, self)
        self.svHistory = ScrollView()
        self.dbOptions = DropDown()
        self.btnSelect = Button(text='Selecteer Parameter', size_hint_y=None, height=30)
        self.build()
        self.callback = True
        self.update([])

    def build(self):
        bltAll = TotalLayout()
        svMain = ScrollView()
        bltCenter = BoxLayout(orientation='vertical')
        bltBottom = BoxLayout(size_hint_y=None, height=36)
        btnExpand = Button(text='Genereer ISP', size_hint_y=None, height=30, on_release=self.expand)
        btnOptimize = Button(text='Optimaal ISP', size_hint_y=None, height=30, on_release=self.minimize)
        self.btnSelect.bind(on_release=self.dbOptions.open)
        for name in self.idp.terms.keys():
            btnTerm = Button(text=name, size_hint_y=None, height=30)
            btnTerm.bind(on_release=lambda btnTerm: self.dbOptions.select(btnTerm.text))
            self.dbOptions.add_widget(btnTerm)
        self.dbOptions.bind(on_select=lambda instance, x: setattr(self.btnSelect, 'text', x))
        btnDistri = Button(size_hint_y=None, height=30, text='ECTS Distributie', on_release=self.show_distribution_popup)
        btnConfirm = Button(size_hint_y=None, height=30, text='Bevestig Selectie', on_release=self.confirm)
        btnReset = Button(size_hint_y=None, height=30, text='Reset', on_release=self.reset)
        bltBottom.add_widget(btnExpand)
        bltBottom.add_widget(btnOptimize)
        bltBottom.add_widget(self.btnSelect)
        bltBottom.add_widget(btnDistri)
        bltBottom.add_widget(btnConfirm)
        bltBottom.add_widget(btnReset)
        svMain.add_widget(self.pnlProgramme)
        bltCenter.add_widget(svMain)
        bltCenter.add_widget(bltBottom)
        bltAll.add_widget(bltCenter)
        bltRight = BoxLayout(size_hint_x=None, width=200, orientation='vertical', spacing=2)
        bltRight.add_widget(HistoryLabel(text='Geschiedenis'))
        bltRight.add_widget(self.svHistory)
        bltRight.add_widget(Button(text='Maak Ongedaan', size_hint_y=None, height=30, on_release=self.show_undo_action_popup))
        bltAll.add_widget(bltRight)
        self.add_widget(bltAll)

    def confirm(self, *args):
        pass #TODO: complete

    def reset(self, *args): #TODO: fix
        self.programme_main = self.programme_init.clone()
        self.programme_temp = self.programme_init.clone()
        self.callback = False
        self.panel.update(self.make_list())
        self.pnlProgramme.refresh()
        self.callback = True
        self.history = list()
        self.update_history()
        self.update([])

    def explain(self, programme):
        i = self.explanation.unsat(self.parser.print_explanation(programme))
        r = self.explanationParser.find_broken_rules(i)
        return r

    def update(self, choices):
        all_old_choices = copy.deepcopy(self.automaton.getAllChoices())
        if self.callback:
            for choice in choices:
                self.update_choice(choice)
            if self.automaton.isConsistent():
                self.step(choices, all_old_choices, copy.deepcopy(self.automaton.getAllChoices()))
            else:
                self.show_unsat_popup(choices)

    def update_choice(self, choice):
        if choice.not_interested:
            self.automaton.addSelection(choice.code, str(0))
        else:
            if choice.selected is not None:
                self.automaton.addSelection(choice.code, str(choice.selected))
            else:
                self.automaton.removeSelection(str(choice.code))

    def propagate(self, programme):
        i = self.parser.print_domain(programme)
        self.updater.filter(i)
        self.updater.filter(self.idp.propagate(i))
        self.updater.update_programme(programme)

    def build_programme(self):
        programme = self.programme_init.clone()
        for code in self.automaton.getAllChoices():
            self.reverse_update_choice(code, self.automaton.getSelection(code), programme)
        return programme

    def reverse_update_choice(self, code, value, programme):
        not_interested = False
        selected = None
        if value == '0':
            not_interested = True
        else:
            selected = int(value)
        programme.update_not_interested(code, not_interested)
        programme.update_selected(code, selected)

    def expand(self, *args):
        i = self.parser.print_domain(self.programme_main)
        self.updater.filter(i)
        self.updater.filter(self.idp.expand(i))
        self.updater.update_programme(self.programme_main)
        self.create_inference_action('ISP gegenereerd')
        self.refresh()

    def minimize(self, *args):
        if 'Select' not in self.btnSelect.text:
            i = self.parser.print_domain(self.programme_main)
            self.updater.filter(i)
            self.updater.filter(self.idp.minimize(self.btnSelect.text, i))
            self.updater.update_programme(self.programme_main)
            self.create_inference_action('ISP geoptimaliseerd (' + self.btnSelect.text + ')')
            self.refresh()

    def refresh(self):
        self.callback = False
        self.panel.update(self.make_list())
        self.pnlProgramme.refresh()
        self.callback = True

    def make_list(self):
        courses = self.programme_main.get_all_courses()
        d = dict()
        for course in courses.values():
            d[course.code] = course.selected
        return d

    def create_user_action(self, choices, ch_old, ch_new, pr_old, pr_new, un_old, un_new):
        if len(choices) > 0:
            self.history.append(UserAction(choices, ch_old, ch_new, pr_old, pr_new, un_old, un_new))
            self.update_history()
        for course in ch_new.values():
            self.programme_main.update_not_interested(course.code, course.not_interested)
            self.programme_main.update_selected(course.code, course.selected)
        for course in pr_new.values():
            self.programme_main.update_not_interested(course.code, course.not_interested)
            self.programme_main.update_selected(course.code, course.selected)
        for course in un_new.values():
            self.programme_main.update_not_interested(course.code, course.not_interested)
            self.programme_main.update_selected(course.code, course.selected)
        self.programme_temp = self.programme_main.clone()

    def create_inference_action(self, inference):
        new = self.programme_main.get_all_courses()
        old = self.programme_temp.get_all_courses()
        before = list()
        after = list()
        for code in new.keys():
            course_new = new.get(code)
            course_old = old.get(code)
            if course_new.selected != course_old.selected or course_new.not_interested != course_old.not_interested:
                before.append(course_old)
                after.append(course_new)
                self.update_choice(course_new)
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
            self.undo_action()
            if isinstance(action, UserAction):
                pr = action.get_propagations()
                if len(pr) > 0:
                    ppUndoAction = UndoActionPopup(action, self)
                    ppUndoAction.open()

    def calculate_solutions(self):
        solutions = list()
        res = self.automaton.calculateRestorations()
        for sol in res:
            sols = dict()
            for code in sol.split(' '):
                sols[code] = self.automaton.getSelection(code)
            solutions.append(sols)
        return solutions

    def show_unsat_popup(self, new_choices):
        programme = self.build_programme()
        solutions = self.calculate_solutions()
        all_choices = list()
        for choice in self.automaton.getAllChoices():
            all_choices.append(self.programme_main.get_course(choice))
        ppUndo = UndoPopup(solutions, new_choices, all_choices, self.explain(programme), self)
        ppUndo.open()

    def show_distribution_popup(self, *args):
        ppDistri = DistributionPopup(self.programme_main.get_ects_distribution(),
                                     self.programme_main.get_min_ects(),
                                     self.programme_main.get_max_ects())
        ppDistri.open()

    def undo_action(self):
        if len(self.history) > 0:
            action = self.history.pop(len(self.history)-1)
            if isinstance(action, UserAction):
                for choice in action.get_old_choices():
                    self.update_choice(choice)
                for undo in action.get_relaxations():
                    self.automaton.removeSelection(undo)
                for course in action.before.values():
                    self.programme_main.update_not_interested(course.code, course.not_interested)
                    self.programme_main.update_selected(course.code, course.selected)
            else:
                for course in action.before:
                    self.automaton.removeSelection(course.code)
                    self.programme_main.update_not_interested(course.code, course.not_interested)
                    self.programme_main.update_selected(course.code, course.selected)
            self.programme_temp = self.programme_main.clone()
            self.refresh()
            self.update_history()

    def step(self, choices, all_old_choices, all_new_choices):
        programme = self.build_programme()
        temp = list()
        for course in choices:
            temp.append(course.code)
        self.propagate(programme)
        ch_new, pr_new, un_new = self.split_courses(programme.get_all_courses(), all_new_choices.keys())
        ch_old, pr_old, un_old = self.split_courses(self.programme_temp.get_all_courses(), all_old_choices.keys())
        # LOOK FOR VALUES THAT ARE NO LONGER PROPAGATED (where to put them?)
        res_old = list()
        res_new = list()
        for code in un_new.keys():
            if code not in temp:
                if code in pr_old.keys():
                    res_old.append(pr_old[code])
                    res_new.append(un_new[code])
        #IF NO UNDONE PROPAGATIONS, FINISH ACTION AND STORE IT
        if len(res_old) == 0:
            self.create_user_action(choices, ch_old, ch_new, pr_old, pr_new, un_old, un_new)
            self.refresh()
        else:
            ppProp = PropagationPopup(choices, res_new, res_old, self)
            ppProp.open()

    def split_courses(self, courses, codes):
        choices = dict()
        propagations = dict()
        unknowns = dict()
        for code in courses.keys():
            course = courses.get(code)
            if code not in codes:
                if course.selected is None and course.not_interested is False:
                    unknowns[code] = course
                else:
                    propagations[code] = course
            else:
                choices[code] = course
        return choices, propagations, unknowns