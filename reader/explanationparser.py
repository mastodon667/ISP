#LOCATION = '/home/herbert/PycharmProjects/Thesis/idp/'
LOCATION = 'C:/Users/Herbert/PycharmProjects/ISP/'

class ExplanationParser(object):

    def __init__(self):
        self.rules = dict()
        with open(LOCATION + 'idp/explanation/rules.txt') as data:
            for line in data:
                rule, explanation = line.split(':')
                self.rules[rule] = explanation

    def find_broken_rules(self, input):
        s = ''
        for line in input.split('\n'):
            if 'satisfied<ct> = ' in line:
                s += self.parse_line(line)
        return s

    def parse_line(self, line):
        s = ''
        for rule in self.rules.keys():
            if rule in line:
                s = self.rules.get(rule) + '\n'
        return s
