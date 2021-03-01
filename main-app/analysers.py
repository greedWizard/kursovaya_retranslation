from structures import Program, Lexem, IdentifierKW, LexError, FOLLOWING_MATRIX, get_define_pattern, unique_identifiers, SymanticError
import structures
import re
import inspect
import sys



def get_structures():
    structs = []
    classes = inspect.getmembers(sys.modules['structures'], inspect.isclass)
    for _class in classes:
        if _class[0].endswith('KW'):
            structs.append(_class[1])

    return structs


class PreProcessor:
    def __init__(self, program: Program):
        self.program = program
        self.process()

    def process(self):
        lexems = []
        bracets = r'(\{|\}|\(|\)|\)|\,|^end\.{1}$)'

        for i in range(len(self.program.lines)):
            self.program.lines[i] = self.program.lines[i].replace('end.', 'end .')
            found_comments = re.findall(
                r'\/\*.*\*\/', self.program.lines[i]
            )

            for comment in found_comments: 
                self.program.lines[i] = self.program.lines[i].replace(
                    comment, ''
                )

            found_bracets = re.findall(bracets, self.program.lines[i])
            
            for bracet in found_bracets:
                self.program.lines[i] = self.program.lines[i].replace(bracet, f' {bracet} ')
            
            found_spaces = re.findall(r'\s+', self.program.lines[i])
            
            for space in found_spaces:
                self.program.lines[i] = self.program.lines[i].replace(space, ' ')

            for lexem in self.program.lines[i].split(' '):
                if lexem != '':
                    lexems.append((Lexem(lexem), i))

        self.lexems = lexems


class Analyser:
    def __init__(
        self,
        preProcessor: PreProcessor,
    ):
        self.preProcessor = preProcessor

    def get_lexems(self):
        self.lexical_analyse()

        return self.lexems

    def _find_last(self, lexem_name):
        last = None
        prev = None

        for lexem in self.lexems:
            if lexem.name == lexem_name:
                last = lexem
                break
        
        return last

    def _check_structure(self):
        starting = r'^program var .+ begin'
        struct = re.findall(starting, self.preProcessor.program.text)
        init = len(struct)
        print(struct)
        if init != 1:
            raise SyntaxError('Синтаксическая ошибка: нарушена структура программы')

    def _find_errors(self):
        self._check_structure
        bracets = r'(\{|\}|\(|\)|\)|\,|^end$|^begin$)'
        errors = []

        self.begins = 0
        self.ends = 0
        self.bracets_op = 0
        self.curl_bracets_op = 0
        self.bracets_cl = 0
        self.curl_bracets_cl = 0
        self.loop = 0
        self.nxt = 0
        self.sqr_bracket_close = 0
        self.sqr_bracket_open = 0
        self.whl = 0
        self.prgm = 0

        for lexem in self.lexems:
            if lexem.name == 'begin':
                self.begins += 1
            elif lexem.name == 'end':
                self.ends += 1
            elif lexem.name == '{':
                self.curl_bracets_op += 1
            elif lexem.name == '}':
                self.curl_bracets_cl += 1
            elif lexem.name == '(':
                self.bracets_op += 1
            elif lexem.name == ')':
                self.bracets_cl += 1
            elif lexem.name == 'loop':
                self.loop += 1
            elif lexem.name == 'next':
                self.nxt += 1
            elif lexem.name == '[':
                self.sqr_bracket_open += 1
            elif lexem.name == ']':
                self.sqr_bracket_close += 1
            elif lexem.name == 'while':
                self.whl += 1
            elif lexem.name == 'program':
                self.prgm += 1

        error = None

        if self.curl_bracets_cl > self.curl_bracets_op:
            error = self._find_last('}')
        if self.curl_bracets_cl < self.curl_bracets_op:
            error = self._find_last('{')
        if self.bracets_cl > self.bracets_op:
            error = self._find_last(')')
        if self.bracets_cl < self.bracets_op:
            error = self._find_last('(')
        if self.ends > self.begins:
            error = self._find_last('end')
        if self.ends < self.begins:
            error = self._find_last('begin')
        if self.whl < self.loop:
            error = self._find_last('loop')
        if self.whl > self.loop:
            error = self._find_last('while')
        
        if error:
            raise SyntaxError(f'Ошибка в строке {error.line}: {error.line_text} -> {error.name} - ошибка синтаксиса')
    
    def _check_syntax(self):
        i = 0
        checked = []
        while i < len(self.lexems):
            if i > 0 and (
                self.lexems[i].TYPE == 'operation' and self.lexems[i-1].TYPE == 'keyword'
            ):
                raise SyntaxError(f'Ошибка в строке {self.lexems[i].line}: {self.lexems[i].line_text} -> {self.lexems[i].name} Ошибка синтаксиса')

            last_i = i
            matched_len = 0
            for seq in FOLLOWING_MATRIX:
                matched = True
                for j in range(len(seq)):
                    if seq[j].REGEX != self.lexems[i].REGEX:
                        matched = False
                        matched_len = 0
                        i = last_i
                        break
                    i += 1
                    matched_len += 1
                if matched_len == len(seq):
                    break
            if not matched:
                raise SyntaxError(f'Ошибка в строке {self.lexems[i].line}: {self.lexems[i].line_text} -> {self.lexems[i].name} Ошибка синтаксиса')

    def lexical_analyse(self):
        lexems = []

        for lexem in self.preProcessor.lexems:
            matched = False
            for _class in get_structures():
                new_lexem = _class(lexem[1]+1, self.preProcessor.program.lines[lexem[1]], lexem[0].name)
                if re.match(_class.REGEX, lexem[0].name):
                    lexems.append(new_lexem)
                    matched = True
            if not matched:
                raise LexError(f'Ошибка в строке {new_lexem.line}: "{new_lexem.line_text}" -> {new_lexem.name} - неопознанная лексема.')

        self.lexems = lexems

    def syntax_analyse(self):
        self._check_structure()
        self._find_errors()

        self._check_syntax()

    def get_identifiers(self):
        identifiers = []

        for lexem in self.lexems:
            if lexem.REGEX == IdentifierKW.REGEX:
                identifiers.append(lexem)

        identifiers = unique_identifiers(identifiers)

        return identifiers

    def _check_defined_idents(self, identifiers):
        full_text = self.preProcessor.program.text.replace('\n', ' ')

        for ident in identifiers:
            pattern = get_define_pattern(ident).replace('^', '').replace('$', '')
            defined_num = len(re.findall(pattern, full_text))

            if defined_num == 0:
                raise SymanticError(f'Ошибка в строке {ident.line}: "{ident.line_text}" -> {ident.name} - Необъявленный идентификатор')
            if defined_num > 1:
                raise SymanticError(f'Ошибка в строке {ident.line}: "{ident.line_text}" -> {ident.name} - Многократное объявление')

    def symantic_analyse(self):
        identifiers = self.get_identifiers()
        self._check_defined_idents(identifiers)
        