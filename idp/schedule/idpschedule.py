#IDP_LOCATION = '/usr/local/bin/idp'
IDP_LOCATION = 'C:/Program Files/idp 3.5.0/bin/idp.bat'
#LOCATION = '/home/herbert/PycharmProjects/Thesis/idp/'
LOCATION = 'C:/Users/Herbert/PycharmProjects/ISP/'

from subprocess import Popen, PIPE


class IDPSchedule(object):

    def __init__(self):
        self.pwd = IDP_LOCATION
        self.inferences = dict()
        with open(LOCATION + 'idp/schedule/inference.txt') as data:
            for line in data:
                name, code = line.split(';')
                self.inferences[name] = code
        self.vocabulary = ''
        with open(LOCATION + 'idp/schedule/vocabulary.txt') as data:
            for line in data:
                self.vocabulary += line + '\n'
        self.theory = ''
        with open(LOCATION + 'idp/schedule/theory.txt') as data:
            for line in data:
                self.theory += line + '\n'
        self.terms = dict()
        with open(LOCATION + 'idp/schedule/terms.txt') as data:
            for line in data:
                name, rule = line.split(';')
                self.terms[name] = rule

    def build(self, structure, inference):
        inp = ''
        inp += 'vocabulary V { \n'
        inp += self.vocabulary + '\n}\n\n'
        inp += 'Theory T : V { \n'
        inp += self.theory + '\n}\n\n'
        inp += 'Structure S : V { \n'
        inp += structure + '\n}\n\n'
        inp += 'Procedure main() { \n'
        inp += self.inferences.get(inference) + '\n}\n\n'
        return inp

    def expand(self, structure):
        inp = self.build(structure, 'expansion')
        return self.open(inp)

    def minimize(self, term, structure):
        inp = self.build(structure, 'minimization')
        inp += 'Term O : V { \n'
        inp += self.terms.get(term) + '\n}\n\n'
        return self.open(inp)

    def open(self, inp):
        idp = Popen(self.pwd, stdin=PIPE, stdout=PIPE)
        out, err = idp.communicate(inp)
        return out
