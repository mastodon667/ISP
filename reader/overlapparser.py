class Parser(object):

    def __init__(self):
        self.replace = ['<ct>', '=', '{', '}', ' ', '\"']

    def parse_total_overlap(self, input):
        for line in input.split('\n'):
            if 'overlap' in line:
                line = line.replace('overlap = {', '')
                for t in self.replace:
                    line = line.replace(t, '')
                return self.parse_line(line)
        return 0

    def parse_line(self, line):
        overlap = 0
        for item in line.split(';'):
            if item != '':
                t,o = item.split('->')
                if o != '':
                    overlap += int(o)
        return overlap/2