class Action(object):
    pass


class UserAction(Action):

    def __init__(self, choices, ch_old, ch_new, pr_old, pr_new, un_old, un_new):
        super(UserAction, self).__init__()
        self.choices = choices
        self.choices_old = list()
        self.choices_new = list()
        self.prop_old = list()
        self.prop_new = list()
        self.unknown_old = list()
        self.unknown_new = list()
        self.before = dict()
        self.after = dict()
        self.setup(ch_old, ch_new, pr_old, pr_new, un_old, un_new)

    def __str__(self):
        s = ''
        for course in self.choices:
            s += '[' + course.code + '] '
            if course.not_interested:
                s += 'Not Interested. '
            elif course.selected is not None:
                s += 'Fase ' + str(course.selected) + '. '
            else:
                s += 'Deselected. '
        return s

    def get_propagations(self):
        propagations = list()
        for code in self.prop_new:
            if code in self.unknown_old:
                propagations.append(self.after[code])
        return propagations

    def get_old_choices(self):
        choices = list()
        for code in self.choices_old:
            choices.append(self.before[code])
        return choices

    def get_relaxations(self):
        relax = list()
        for code in self.choices_new:
            if code not in self.choices_old:
                relax.append(code)
        return relax

    def setup(self, ch_old, ch_new, pr_old, pr_new, un_old, un_new):
        for code in ch_old:
            if code in ch_new:
                if ch_old[code] != ch_new[code]:
                    self.before[code] = ch_old[code]
                    self.after[code] = ch_new[code]
                    self.choices_old.append(code)
                    self.choices_new.append(code)
            elif code in pr_new:
                if ch_old[code] != pr_new[code]:
                    self.before[code] = ch_old[code]
                    self.after[code] = pr_new[code]
                    self.choices_old.append(code)
                    self.prop_new.append(code)
            elif code in un_new:
                if ch_old[code] != un_new[code]:
                    self.before[code] = ch_old[code]
                    self.after[code] = un_new[code]
                    self.choices_old.append(code)
                    self.unknown_new.append(code)
        for code in pr_old:
            if code in ch_new:
                if pr_old[code] != ch_new[code]:
                    self.before[code] = pr_old[code]
                    self.after[code] = ch_new[code]
                    self.prop_old.append(code)
                    self.choices_new.append(code)
            elif code in pr_new:
                if pr_old[code] != pr_new[code]:
                    self.before[code] = pr_old[code]
                    self.after[code] = pr_new[code]
                    self.prop_old.append(code)
                    self.prop_new.append(code)
            elif code in un_new:
                if pr_old[code] != un_new[code]:
                    self.before[code] = pr_old[code]
                    self.after[code] = un_new[code]
                    self.prop_old.append(code)
                    self.unknown_new.append(code)
        for code in un_old:
            if code in ch_new:
                if un_old[code] != ch_new[code]:
                    self.before[code] = un_old[code]
                    self.after[code] = ch_new[code]
                    self.unknown_old.append(code)
                    self.choices_new.append(code)
            elif code in pr_new:
                if un_old[code] != pr_new[code]:
                    self.before[code] = un_old[code]
                    self.after[code] = pr_new[code]
                    self.unknown_old.append(code)
                    self.prop_new.append(code)

class InferenceAction(Action):

    def __init__(self, inference, after, before):
        super(InferenceAction, self).__init__()
        self.before = before
        self.inference = inference
        self.after = after

    def __str__(self):
        return self.inference
