IDP_LOCATION = "/usr/local/bin/idp"

from subprocess import Popen, PIPE


class IDPISP(object):

    def __init__(self):
        self.pwd = IDP_LOCATION
        self.inferences = dict()
        with open('/home/herbert/PycharmProjects/Thesis/idp/isp/inference.txt') as data:
            for line in data:
                name, code = line.split(';')
                self.inferences[name] = code
        self.unsatvoc = ''
        with open('/home/herbert/PycharmProjects/Thesis/idp/isp/unsatvoc.txt') as data:
            for line in data:
                self.unsatvoc += line + '\n'
        self.vocabulary = ''
        with open('/home/herbert/PycharmProjects/Thesis/idp/isp/vocabulary.txt') as data:
            for line in data:
                self.vocabulary += line + '\n'
        self.theory = ''
        with open('/home/herbert/PycharmProjects/Thesis/idp/isp/theory.txt') as data:
            for line in data:
                self.theory += line + '\n'
        self.terms = dict()
        with open('/home/herbert/PycharmProjects/Thesis/idp/isp/terms.txt') as data:
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

    def sat(self, structure):
        inp = self.build(structure, 'sat')
        return 'true' in self.open(inp)

    def unsat(self, structure):
        inp = self.build(structure, 'unsat')
        inp += 'vocabulary U { \n'
        inp += self.unsatvoc + '\n}\n\n'
        return self.open(inp)

    def expand(self, structure):
        inp = self.build(structure, 'expansion')
        return self.open(inp)

    def propagate(self, structure):
        inp = self.build(structure, 'propagation')
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
