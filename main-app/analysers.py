from structures import Program
import structures
import re


class LexicalAnalyser:
    def _detect_type(self, line: str, i: int = None):
        identifier = r'\w{1}\d+\w{1}'
        program_begin = r'program var \w+ begin \w+ \{;'
        types = r'(integer{1}|real{1}|boolean{1})'
        end_program = r'\} end\.' 
        read = r'read.+'
        declare = r'\{' + identifier + r', \{, ' + identifier + r' ' + types + r'\}\}'
        ops_begin = r'begin .+'
        ops_end = r'}end'
        operations = r'(\+{1}|\-{1}|/|\*)'
        consts = r'(' + identifier + r'|\d+\.{1}\d+|true|false|\d+)'
        asg = identifier + r' ass ' + consts + r'(' + operations + consts + r')*'
        keywords = r'(ass|program var|begin|end|read|end\.|do while|for|if|then)'

        kws = re.findall(keywords, line)

        if len(kws) > 0 :
            self.append_kws(kws, i, line)

        if re.match(asg, line):
            idents = re.findall(identifier, line)
            self.append_idents(idents, i, line)
            return 'Assignment', idents[0]
        elif re.match(identifier, line):
            return 'Identifier', re.match(identifier, line).group()
        elif re.match(program_begin, line):
            name = line.split(' ')[2].split('begin')[0]
            return 'ProgramBegin', name
        elif re.match(types, line):
            return 'Type', re.match(types, line).group()
        elif re.match(end_program, line):
            return 'EndProgram', ''
        elif re.match(read, line):
            idents = re.findall(identifier, line)
            self.append_idents(idents, i, line)
            return 'Read', ''
        elif re.match(declare, line):
            idents = re.findall(identifier, line)
            self.append_idents(idents, i, line)
            return 'Declare', ''
        elif re.match(ops_begin, line):
            return 'OpsBegin', ''
        elif re.match(ops_end, line):
            return 'OpsEnd', ''
    
    def append_idents(self, idents: list, i: int, line: str):
        for name in idents:
            name = name.replace('}', '').replace(')', '').replace('{', '').replace(')', '').replace(', ', '')
            self.append_el('Identifier', i, line, name)

    def append_kws(self, kws: list, i: int, line: str):
        for kw in kws:
            kw = kw.replace('}', '').replace(')', '').replace('{', '').replace(')', '').replace(', ', '')
            self.append_el('KeyWord', i, line, kw)

    def __init__(self, program: Program):
        self.program = program
        self.unrec_comps = []

        for line in self.program:
            self.unrec_comps.append(line)

        self.rec_compos = []

    def _format_line(self, line: str):
        p = r'\W{1}'
        r = list(set(re.findall(p, line)))

        try:
            r.remove(' ')
        except ValueError:
            print(r)

        for e in r:
            line = line.replace(e, '')

        line.replace(' ', ' ')
        line = re.sub(' +', ' ', line)
        return line

    def _try_parse(self, line: str, i: int):
        line = self._format_line(line)
        lines = line.split(' ')

        for l, i in zip(lines, range(len(lines))):
            try:
                structure, name = self._detect_type(l, i)
            except TypeError:
                raise structures.LexException(f'Не удалось обработать {line}')
            else:
                self.append_el(structure, i, line, name)


    def append_el(self, structure: str, line: int, line_text: str, name: str = ''):
        self.rec_compos.append(getattr(structures, structure)(
                line = line,
                line_text = line_text,
                name = name,
            ))

    def start(self):
        for i in range(len(self.program)):
            line = self.program[i].rstrip().lstrip()

            if len(line) == 0:
                continue

            try:
                structure, name = self._detect_type(line)
            except TypeError:
                self._try_parse(line, i)
                continue
            self.append_el(structure, i, line, name)
