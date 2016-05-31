class Group(object):

    def __init__(self, name, type, min, max, stages):
        self.name = name
        self.type = type
        self.mandatory_courses = list()
        self.optional_courses = list()
        self.min = min
        self.max = max
        self.groups = list()
        self.stages = stages

    def add_group(self, group):
        self.groups.append(group)

    def add_mandatory_course(self, course):
        self.mandatory_courses.append(course)

    def add_optional_course(self, course):
        self.optional_courses.append(course)

    def print_is_type(self):
        s = ''
        s += str(self.name) + ',' + str(self.type) + ';'
        for group in self.groups:
            s += group.print_is_type()
        return s

    def print_mandatory_courses(self):
        s = ''
        for course in self.mandatory_courses:
            s += str(course.code) + ',' + str(self.name) + ';'
        for group in self.groups:
            s += group.print_mandatory_courses()
        return s

    def print_in_group(self):
        s = ''
        for course in self.mandatory_courses:
            s += str(course.code) + ',' + str(self.name) + ';'
        for course in self.optional_courses:
            s += str(course.code) + ',' + str(self.name) + ';'
        for group in self.groups:
            s += group.print_in_group()
        return s

    def print_min_ects(self):
        s = ''
        s += str(self.name) + '-> ' + str(self.min) + ';'
        for group in self.groups:
            s += group.print_min_ects()
        return s

    def print_max_ects(self):
        s = ''
        s += str(self.name) + '-> ' + str(self.max) + ';'
        for group in self.groups:
            s += group.print_max_ects()
        return s

    def print_amount_of_ects(self):
        s = ''
        for course in self.mandatory_courses:
            s += course.print_amount_of_ects()
        for course in self.optional_courses:
            s += course.print_amount_of_ects()
        for group in self.groups:
            s += group.print_amount_of_ects()
        return s

    def print_in_stage(self):
        s = ''
        for course in self.mandatory_courses:
            s += course.print_in_stage()
        for course in self.optional_courses:
            s += course.print_in_stage()
        for group in self.groups:
            s += group.print_in_stage()
        return s

    def print_in_term(self):
        s = ''
        for course in self.mandatory_courses:
            s += course.print_in_term()
        for course in self.optional_courses:
            s += course.print_in_term()
        for group in self.groups:
            s += group.print_in_term()
        return s

    def print_course(self):
        s = ''
        for course in self.mandatory_courses:
            s += str(course.code) + ';'
        for course in self.optional_courses:
            s += str(course.code) + ';'
        for group in self.groups:
            s += group.print_course()
        return s

    def print_group(self):
        s = ''
        s += self.name + ';'
        for group in self.groups:
            s += group.print_group()
        return s

    def print_selected(self):
        s = ''
        for course in self.mandatory_courses:
            s += course.print_selected()
        for course in self.optional_courses:
            s += course.print_selected()
        for group in self.groups:
            s += group.print_selected()
        return s

    def print_not_interested(self):
        s = ''
        for course in self.mandatory_courses:
            s += course.print_not_interested()
        for course in self.optional_courses:
            s += course.print_not_interested()
        for group in self.groups:
            s += group.print_not_interested()
        return s

    def update_selected(self, code, value):
        for course in self.mandatory_courses:
            if course.update_selected(code, value):
                return True
        for course in self.optional_courses:
            if course.update_selected(code, value):
                return True
        for group in self.groups:
            if group.update_selected(code, value):
                return True
        return False

    def update_not_interested(self, code, value):
        for course in self.mandatory_courses:
            if course.update_not_interested(code, value):
                return True
        for course in self.optional_courses:
            if course.update_not_interested(code, value):
                return True
        for group in self.groups:
            if group.update_not_interested(code, value):
                return True
        return False

    def get_ects_distribution(self):
        distribution = dict()
        count = 0
        for course in self.mandatory_courses:
            if course.selected is not None:
                count += course.ects
        for course in self.optional_courses:
            if course.selected is not None:
                count += course.ects
        for group in self.groups:
            distr = group.get_ects_distribution()
            for name in distr:
                count += distr[name]
                distribution[name] = distr[name]
        distribution[self.name] = count
        return distribution

    def get_min_ects(self):
        minimum = dict()
        minimum[self.name] = self.min
        for group in self.groups:
            temp = group.get_min_ects()
            for name in temp.keys():
                minimum[name] = temp.get(name)
        return minimum

    def get_max_ects(self):
        maximum = dict()
        maximum[self.name] = self.max
        for group in self.groups:
            temp = group.get_max_ects()
            for name in temp.keys():
                maximum[name] = temp.get(name)
        return maximum

    def get_course(self, code):
        for course in self.mandatory_courses:
            if course.code == code:
                return course
        for course in self.optional_courses:
            if course.code == code:
                return course
        for group in self.groups:
            course = group.get_course(code)
            if course is not None:
                return course
        return None

    def clone(self):
        g = Group(self.name, self.type, self.min, self.max, self.stages)
        for course in self.mandatory_courses:
            g.add_mandatory_course(course.clone())
        for course in self.optional_courses:
            g.add_optional_course(course.clone())
        for group in self.groups:
            g.add_group(group.clone())
        return g

    def get_all_courses(self):
        courses = dict()
        for course in self.mandatory_courses:
            courses[course.code] = course.clone()
        for course in self.optional_courses:
            courses[course.code] = course.clone()
        for group in self.groups:
            for course in group.get_all_courses().values():
                courses[course.code] = course
        return courses

    def get_selected_courses(self):
        courses = list()
        for course in self.mandatory_courses:
            if course.selected is not None:
                courses.append(course.code)
        for course in self.optional_courses:
            if course.selected is not None:
                courses.append(course.code)
        for group in self.groups:
            for code in group.get_selected_courses():
                courses.append(code)
        return courses