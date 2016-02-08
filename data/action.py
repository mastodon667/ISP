class Action(object):

    def __init__(self, before):
        self.before = before

    def get_course_before(self, code):
        for course in self.before:
            if course.code == code:
                return course
        return None


class UserAction(Action):

    def __init__(self, choices, propagations, before):
        super(UserAction, self).__init__(before)
        self.choices = choices
        self.propagations = propagations

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


class InferenceAction(Action):

    def __init__(self, inference, after, before):
        super(InferenceAction, self).__init__(before)
        self.inference = inference
        self.after = after

    def __str__(self):
        return self.inference
