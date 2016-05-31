class Updater(object):

    def __init__(self):
        self.selected_old = dict()
        self.not_interested_old = dict()
        self.replace = ['<ct>', '=', '{', '}', ' ', '\"']

    def update_selected(self, selected_new):
        for course in self.selected_old.keys():
            if course in selected_new.keys():
                self.selected_old[course] = selected_new.get(course)
            else:
                self.selected_old[course] = None
        for course in selected_new.keys():
            if course not in self.selected_old.keys():
                self.selected_old[course] = selected_new.get(course)

    def update_not_interested(self, not_interested_new):
        for course in self.not_interested_old.keys():
            if course in not_interested_new.keys():
                self.not_interested_old[course] = True
            else:
                self.not_interested_old[course] = False
        for course in not_interested_new.keys():
            if course not in self.not_interested_old.keys():
                self.not_interested_old[course] = not_interested_new.get(course)

    def update_programme(self, programme):
        for course in self.selected_old.keys():
            programme.update_selected(course, self.selected_old.get(course))
        for course in self.not_interested_old.keys():
            programme.update_not_interested(course, self.not_interested_old.get(course))
        self.selected_old = dict()
        self.not_interested_old = dict()

    def filter(self, text):
        for line in text.split('\n'):
            if 'NietGeselecteerd ' in line:
                self.update_not_interested(self.return_not_interested(line))
            elif 'NietGeselecteerd<ct>' in line:
                self.update_not_interested(self.return_not_interested(line))
            elif 'Geselecteerd<ct>' in line:
                self.update_selected(self.return_selected(line))
            elif 'Geselecteerd ' in line:
                self.update_selected(self.return_selected(line))

    def get_unsat(self, text):
        codes = set()
        for line in text.split('\n'):
            if 'NietGeselecteerd ' in line:
                for code in self.return_not_interested(line).keys():
                    codes.add(code)
            elif 'NietGeselecteerd<ct>' in line:
                for code in self.return_not_interested(line).keys():
                    codes.add(code)
            elif 'Geselecteerd ' in line:
                for code in self.return_selected(line).keys():
                    codes.add(code)
            elif 'Geselecteerd<ct>' in line:
                for code in self.return_selected(line).keys():
                    codes.add(code)
        return codes

    def return_not_interested(self, line):
        result = dict()
        newLine = self.filter_string(line.replace('NietGeselecteerd', ''))
        for course in newLine.split(';'):
            course = course.lstrip().rstrip()
            if not course == '':
                result[course] = True
        return result

    def return_selected(self, line):
        result = dict()
        newLine = self.filter_string(line.replace('Geselecteerd', ''))
        for item in newLine.split(';'):
            item = item.lstrip().rstrip()
            if not item == '':
                course, value = item.split(',')
                result[course] = int(value)
        return result

    def filter_string(self, line):
        for s in self.replace:
            line = line.replace(s, '')
        return line
