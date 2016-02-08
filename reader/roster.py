from data.course import Class
from datetime import *


class Roster(object):

    def __init__(self, url, input, codes):
        self.url = url
        self.input = input
        self.codes = codes

    def parse(self):
        all_classes = dict()
        for code in self.codes:
            all_classes[code] = self.parse_course(code)
        return all_classes

    def parse_course(self, code):
        classes = list()
        with open(self.url + self.input) as data:
            for line in data:
                c = self.parse_line(line, code)
                if c is not None:
                    classes.append(c)
        return classes

    def parse_line(self, line, code):
        items = line.split('|')
        if items[10] != code:
            return None
        return self.parse_class(items[2], items[3], items[4], items[6], items[7], items[8], items[10],
                                items[18], items[19], items[22], items[32], items[35], items[38])

    def parse_class(self, event_nr, week, date, start, end, ects_d, code,
                    building, room_nr, room_name, teacher, notes, group_info):
        return Class(int(event_nr), int(week[-2:]), code, ects_d, self.parse_date(date, start),
                     self.parse_date(date, end), building, room_nr, room_name, teacher, notes, group_info)

    def parse_date(self, date, time):
        temp1 = date.split('.')
        temp2 = time.split(':')
        print(date)
        print(time)
        return datetime(year=int(temp1[2]), month=int(temp1[1]), day=int(temp1[0]),
                        hour=int(temp2[0]), minute=int(temp2[1]))
