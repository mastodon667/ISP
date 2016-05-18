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

    def convert(self, pos, variables, node, graph, seen):
        state = None
        if node in seen:
            state = seen[node]
        else:
            if pos < len(variables):
                state = State(variables[pos].strip('\n'), 1)
            else:
                state = State('', 0)
            seen[node] = state
            for neighbor in graph.neighbors(node):
                state.addoTransition(Transition(graph.edge_label((node, neighbor)),
                                                self.convert(pos + 1, variables, neighbor, graph, seen)))
        return state

    def initial_node(self):
        return self.dgraph.neighbors('initial')[0]


if __name__ == '__main__':
    r = Reader()
    g = r.dgraph
    i = r.initial_node()
    vars = list()
    with open('C:/Users/Herbert/PycharmProjects/ISP/automaton/variables.txt', 'r') as dotFile:
        vars = dotFile.readlines()
    for s in vars:
        s = s.strip('\n')
    iState = r.convert(0, vars, i, g, dict())
    isp = Automaton(iState)
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