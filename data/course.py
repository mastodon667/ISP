class Course(object):
    def __init__(self, code, name, ects, stages, term, selected, not_interested):
        self.code = code
        self.name = name
        self.ects = ects
        self.stages = list()
        self.selected = selected
        self.not_interested = not_interested
        for item in stages:
            self.stages.append(item)
        self.term = term

    def print_amount_of_ects(self):
        return str(self.code) + '-> ' + str(self.ects) + ';'

    def print_in_stage(self):
        s = ''
        for item in self.stages:
            s += str(self.code) + ',' + str(item) + ';'
        return s

    def print_in_term(self):
        t = ''
        if self.term == 1:
            t += 'Eerste'
        elif self.term == 2:
            t += 'Tweede'
        else:
            t += 'Jaar'
        return str(self.code) + '-> ' + str(t) + ';'

    def set_not_interested(self, value):
        self.not_interested = value
        if value:
            self.selected = None

    def set_selected(self, value):
        self.selected = value

    def print_selected(self):
        if self.selected is not None:
            return self.code + ',' + str(self.selected) + ';'
        return ''

    def print_not_interested(self):
        if self.not_interested:
            return self.code + ';'
        return ''

    def update_selected(self, code, value):
        if code == self.code:
            self.selected = value
            if value is not None:
                self.not_interested = False
            return True
        return False

    def update_not_interested(self, code, value):
        if code == self.code:
            self.not_interested = value
            if value:
                self.selected = None
            return True
        return False

    def clone(self):
        return Course(self.code, self.name, self.ects, self.stages, self.term, self.selected, self.not_interested)

    def __str__(self):
        s = '[' + self.code + '] ' + self.name + ': '
        if self.selected is not None:
            s += 'stage ' + str(self.selected)
        elif self.not_interested:
            s += ' not interested'
        return s

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Course):
            return False
        if other.code != self.code:
            return False
        if other.name != self.name:
            return False
        if other.stages != self.stages:
            return False
        if other.selected != self.selected:
            return False
        if other.not_interested != self.not_interested:
            return False
        return True


class Class(object):
    # 1,5,3,10,8,(4,6),(4,7),18,19,22,32,35,38
    def __init__(self, event_id, weekday, week, code, ects_d, start, end, building, room_nr, room_name, teacher, notes,
                 group_info):
        self.event_id = event_id
        self.weekday = weekday
        self.week = week
        self.code = code
        self.ects_d = ects_d
        self.start = start
        self.end = end
        self.building = building
        self.room_nr = room_nr
        self.room_name = room_name
        self.teacher = teacher
        self.notes = notes
        self.group_info = group_info

    def get_duration(self):
        duration = self.end - self.start
        return duration.total_seconds() / 3600

    def get_start(self):
        slot = self.weekday*26
        slot += (self.start.hour-8)*2
        if self.start.minute >= 30:
            slot += 1
        return slot

    def get_end(self):
        slot = self.weekday*26
        slot += (self.end.hour-8)*2
        if self.end.minute >= 30:
            slot += 1
        return slot

    def __str__(self):
        s = 'Course: ' + self.code + ' - ' + self.notes + ' ' + self.group_info + '\n'
        s += 'Class #' + str(self.event_id) + ' in week ' + str(self.week) + '\n'
        s += 'Teacher: ' + self.teacher + '\n'
        s += 'Location: ' + self.building + ' ' + self.room_nr + '(' + self.room_name + ')' + '\n'
        s += 'From: ' + str(self.start) + 'Until: ' + str(self.end) + '\n\n'
        return s
