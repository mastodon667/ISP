from data.course import Class
from data.schedule import CourseSchedule
from datetime import *


class Roster(object):

    def __init__(self, url, input, shadow):
        self.url = url
        self.shadow = shadow
        self.input = input

    def parse_course(self, code):
        schedule = CourseSchedule(code)
        codes = self.find_shadowcourse(code)
        for i in self.input:
            with open(self.url + i) as data:
                for line in data:
                    c = self.parse_line(line, codes)
                    if c is not None:
                        schedule.add_class(c)
        return schedule

    def parse_line(self, line, codes):
        items = line.split('|')
        if items[10] not in codes:
            return None
        return self.parse_class(items[1], items[5], items[3], items[4], items[6], items[7], items[8], items[10],
                                items[18], items[19], items[22], items[32], items[35], items[38])

    def parse_class(self, event_id, weekday, week, date, start, end, ects_d, code,
                    building, room_nr, room_name, teacher, notes, group_info):
        i = 0
        if 'Maandag' in weekday:
            i = 0
        if 'Dinsdag' in weekday:
            i = 1
        if 'Woensdag' in weekday:
            i = 2
        if 'Donderdag' in weekday:
            i = 3
        if 'Vrijdag' in weekday:
            i = 4
        return Class(int(event_id), i, int(week[-2:]), code, ects_d, self.parse_date(date, start),
                     self.parse_date(date, end), building, room_nr, room_name, teacher, notes, group_info)

    def find_shadowcourse(self, code):
        codes = list()
        codes.append(code)
        with open(self.url + self.shadow) as data:
            for line in data:
                c1, c2 = line.split(',')
                if c1 == code:
                    codes.append(c2)
        return codes

    def parse_date(self, date, time):
        temp1 = date.split('.')
        temp2 = time.split(':')
        return datetime(year=int(temp1[2]), month=int(temp1[1]), day=int(temp1[0]),
                        hour=int(temp2[0]), minute=int(temp2[1]))
