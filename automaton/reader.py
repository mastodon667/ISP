from pygraph.classes.digraph import digraph
from pygraph.readwrite import dot

class Reader(object):

    def __init__(self):
        s = ''
        with open('C:/Users/Herbert/PycharmProjects/ISP/automaton/automaton_dot.gv', 'r') as dotFile:
            s += dotFile.read()
        self.dgraph = dot.read(s)

    def convert(self, pos, variables, stateAlt, seen):
        state = None
        if stateAlt in seen:
            state = seen[stateAlt]
        else:
            if pos < len(variables):
                state = State(variables[pos], 1)
            else:
                state = State('', 0)
            seen[stateAlt] = state

    def initial_node(self):
        for node in self.dgraph.nodes():
            if len(self.dgraph.incidents(node)) == 0:
                return node

if __name__ == '__main__':
    r = Reader()
    g = r.dgraph
    i = r.initial_node()
    print(str(i))
    print('incidents: ' + str(g.incidents(i)))