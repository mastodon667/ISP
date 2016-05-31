#IDP_LOCATION = '/usr/local/bin/idp'
IDP_LOCATION = 'C:/Program Files/idp 3.5.0/bin/idp.bat'
#LOCATION = '/home/herbert/PycharmProjects/Thesis/idp/'
LOCATION = 'C:/Users/Herbert/PycharmProjects/ISP/'

import time

from subprocess import Popen, PIPE


class IDPExplanation(object):

    def __init__(self):
        self.pwd = IDP_LOCATION
        self.inferences = dict()
        with open(LOCATION + 'idp/explanation/inference.txt') as data:
            for line in data:
                name, code = line.split(';')
                self.inferences[name] = code
        self.vocabulary = ''
        with open(LOCATION + 'idp/explanation/vocabulary.txt') as data:
            for line in data:
                self.vocabulary += line + '\n'
        self.theory = ''
        with open(LOCATION + 'idp/explanation/theory.txt') as data:
            for line in data:
                self.theory += line + '\n'
        self.unsatstruc = ''
        with open(LOCATION + 'idp/explanation/unsatstruc.txt') as data:
            for line in data:
                self.unsatstruc += line + '\n'
        self.unsatvoc = ''
        with open(LOCATION + 'idp/explanation/unsatvoc.txt') as data:
            for line in data:
                self.unsatvoc += line + '\n'

    def build(self, structure, inference):
        inp = ''
        inp += 'vocabulary V { \n'
        inp += self.vocabulary + '\n}\n\n'
        inp += 'Theory T : V { \n'
        inp += self.theory + '\n}\n\n'
        inp += 'Structure S : V { \n'
        inp += structure + '\n'
        inp += self.unsatstruc + '\n}\n\n'
        inp += 'Vocabulary U { \n'
        inp += self.unsatvoc + '\n}\n\n'
        inp += 'Procedure main() { \n'
        inp += self.inferences.get(inference) + '\n}\n\n'
        return inp

    def unsat(self, structure):
        inp = self.build(structure, 'unsat')
        return self.open(inp)

    def open(self, inp):
        ts = time.time()
        idp = Popen(self.pwd, stdin=PIPE, stdout=PIPE)
        out, err = idp.communicate(inp)
        te = time.time()
        with open(LOCATION + 'reader/results.txt', 'a') as file:
            file.write('explanation - ' + str(te - ts) + '\n')
        return out
