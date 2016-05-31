class CourseSchedule(object):

    def __init__(self, code):
        self.code = code
        self.classes = list()
        self.weeks = set()

    def add_class(self, c):
        for c1 in self.classes:
            if c1.week == c.week:
                if c1.event_id == c.event_id:
                    return None
        self.classes.append(c)
        self.weeks.add(c.week)

    def get_total_duration(self, week):
        duration = 0
        for c in self.classes:
            if c.week == week:
                duration += c.get_duration()
        return duration

    def print_classes(self, week):
        s = ''
        for c in self.classes:
            if c.week == week:
                s += str(c.event_id) + ';'
        return s

    def print_has_class(self, week):
        s = ''
        for c in self.classes:
            if c.week == week:
                s += self.code + ',' + str(c.event_id) + ';'
        return s

    def print_starts(self, week):
        s = ''
        for c in self.classes:
            if c.week == week:
                s += str(c.event_id) + ',' + str(c.get_start()) + ';'
        return s

    def print_ends(self, week):
        s = ''
        for c in self.classes:
            if c.week == week:
                s += str(c.event_id) + ',' + str(c.get_end()) + ';'
        return s


class StageSchedule(object):

    def __init__(self, stage):
        self.stage = stage
        self.courseSchedules = dict()

    def add_schedule(self, code, schedule):
        self.courseSchedules[code] = schedule

    def remove_schedule(self, code):
        if code in self.courseSchedules.keys():
            self.courseSchedules.pop(code)

    def busiest_week(self, term):
        week_start = 27
        week_stop = 52
        if term == 2:
            week_start = 1
            week_stop = 26
        week = week_start
        duration = 0
        for i in range(week_start, week_stop+1):
            d = 0
            for cs in self.courseSchedules.values():
                d += cs.get_total_duration(i)
            if d >= duration:
                week = i
                duration = d
        return week

    def get_schedules(self):
        return self.courseSchedules.values()

    def print_courses(self):
        s = ''
        for code in self.courseSchedules.keys():
            s += code + ';'
        return s

    def print_classes(self, week):
        s = ''
        for schedule in self.courseSchedules.values():
                s += schedule.print_classes(week)
        return s

    def print_has_class(self, week):
        s = ''
        for schedule in self.courseSchedules.values():
            s += schedule.print_has_class(week)
        return s

    def print_starts(self, week):
        s = ''
        for schedule in self.courseSchedules.values():
            s += schedule.print_starts(week)
        return s

    def print_ends(self, week):
        s = ''
        for schedule in self.courseSchedules.values():
            s += schedule.print_ends(week)
        return s


class CompleteSchedule(object):

    def __init__(self, stages):
        self.stageSchedules = dict()
        for i in range(1, stages+1):
            self.stageSchedules[i] = StageSchedule(i)

    def add_schedule(self, courseSchedule, stage):
        self.stageSchedules.get(stage).add_schedule(courseSchedule.code, courseSchedule)
        for stageSchedule in self.stageSchedules.values():
            if not stageSchedule.stage == stage:
                stageSchedule.remove_schedule(courseSchedule.code)

    def remove_schedule(self, code):
        for stageSchedule in self.stageSchedules.values():
            stageSchedule.remove_schedule(code)

    def get_stages(self):
        return self.stageSchedules.keys()

    def get_schedules(self, stage):
        return self.stageSchedules[stage].get_schedules()

    def print_structure(self, stage, term):
        week = self.stageSchedules.get(stage).busiest_week(term)
        strVak = 'Vak = {'
        strSlot = 'Slot = {1..130}'
        strLes = 'Les = {'
        strHeeftLes = 'heeftLes = {'
        strStart = 'start = {'
        strEindigt = 'eindigt = {'
        strVak += self.stageSchedules.get(stage).print_courses()
        strLes += self.stageSchedules.get(stage).print_classes(week)
        strHeeftLes += self.stageSchedules.get(stage).print_has_class(week)
        strStart += self.stageSchedules.get(stage).print_starts(week)
        strEindigt += self.stageSchedules.get(stage).print_ends(week)
        strVak += '}'
        strLes += '}'
        strHeeftLes += '}'
        strStart += '}'
        strEindigt += '}'

        s = ''
        s += strVak + '\n'
        s += strSlot + '\n'
        s += strLes + '\n'
        s += strHeeftLes + '\n'
        s += strStart + '\n'
        s += strEindigt + '\n'
        return s