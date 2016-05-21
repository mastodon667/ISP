from pygraph.classes.digraph import digraph
from pygraph.readwrite import dot
from state import State
from transition import Transition
from automaton import Automaton


class Reader(object):

    def __init__(self):
        s = ''
        with open('C:/Users/Herbert/PycharmProjects/ISP/automaton/automaton_dot.gv', 'r') as dotFile:
            s += dotFile.read()
        self.dgraph = dot.read(s)
        vars = list()
        with open('C:/Users/Herbert/PycharmProjects/ISP/automaton/variables.txt', 'r') as dotFile:
            vars = dotFile.readlines()
        for s in vars:
            s = s.strip('\n')
        self.automaton = Automaton(self.convert(0, vars, self.initial_node(), self.dgraph, dict()))

    def convert(self, pos, variables, node, graph, seen):
        state = None
        if node in seen:
            state = seen[node]
        else:
            if pos < len(variables):
                state = State(variables[pos].strip('\n').lstrip().rstrip(), 1)
            else:
                state = State('', 0)
            seen[node] = state
            for neighbor in graph.neighbors(node):
                for val in graph.edge_label((node, neighbor)).strip('\"').split('-'):
                    state.addoTransition(Transition(val, self.convert(pos + 1, variables, neighbor, graph, seen)))
        return state

    def initial_node(self):
        return self.dgraph.neighbors('initial')[0]

    def getAutomaton(self):
        return self.automaton


if __name__ == '__main__':
    r = Reader()
    print('Finished converting from dot file')
    isp = r.getAutomaton()
    print('Automaton created')
    print('Valid: ' + str(isp.isConsistent()))
    isp.addSelection('G0Q55A', '0')
    print('DESELECTED: Fundamenten van Mens-machine interactie')
    isp.addSelection('H04K5A', '0')
    print('DESELECTED: Development of Secure Software')
    isp.addSelection('C07I6A', '1')
    print('SELECTED: ICT-Recht')
    print('Valid: ' + str(isp.isConsistent()))
    isp.addSelection('H02D2A', '0')
    print('DESELECTED: Uncertainty in Artificial Intelligence')
    print('Valid: ' + str(isp.isConsistent()))
    isp.develop(isp.getInitialState(), '', '')
    isp.showRestoration()
    isp.removeSelection('H02D2A')
    print('DESELECTION UNDONE: Uncertainty in Artificial Intelligence')
    print('Valid: ' + str(isp.isConsistent()))