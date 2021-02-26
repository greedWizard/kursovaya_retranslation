from structures import Program, Lexem, IdentifierKW, LexError, FOLLOWING_MATRIX
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


class LexAnalyser:
    def __init__(self, program: Program):
        self._program = program

    def analyse(self):
        lexems = []
        bracets = r'(\{|\}|\(|\)|\)|\,|^end\.{1}$)'

        for i in range(len(self._program.lines)):
            self._program.lines[i] = self._program.lines[i].replace('end.', 'end .')
            found_comments = re.findall(
                r'\/\*.*\*\/', self._program.lines[i]
            )

            for comment in found_comments: 
                self._program.lines[i] = self._program.lines[i].replace(
                    comment, ''
                )

            found_bracets = re.findall(bracets, self._program.lines[i])
            
            for bracet in found_bracets:
                self._program.lines[i] = self._program.lines[i].replace(bracet, f' {bracet} ')
            
            found_spaces = re.findall(r'\s+', self._program.lines[i])
            
            for space in found_spaces:
                self._program.lines[i] = self._program.lines[i].replace(space, ' ')

            for lexem in self._program.lines[i].split(' '):
                if lexem != '':
                    lexems.append((Lexem(lexem), i))

        self.lexems = lexems


class SyntaxAnalyzer:
    def __init__(
        self,
        lexAnalyser: LexAnalyser,
    ):
        self.lexAnalyser = lexAnalyser

        variable = [
            structures.IdentifierKW, structures.TypeKW
        ]
        description = [
            structures.CurlBracketOpenKW, structures.IdentifierKW, structures.CurlBracketOpenKW,
            structures.ComaKW, variable, 
        ]
        program_struct = [
            structures.ProgramKW, structures.VarKW, description, 
            structures.BeginKW, structures.CurlBracketOpenKW, structures.SemiColumnKW,
            structures.Operator, structures.CurlBracketCloseKW, structures.EndKW,
            structures.DotKW,
        ]

    def _find_errors(self):
        bracets = r'(\{|\}|\(|\)|\)|\,|^end$|^begin$)'
        errors = []
        
        begins = 0
        ends = 0
        bracets_op = 0
        curl_bracets_op = 0
        bracets_cl = 0
        curl_bracets_cl = 0

        for lexem in self.lexems:
            if lexem.name == 'begin':
                begins += 1
            elif lexem.name == 'end':
                ends += 1
            elif lexem.name == '{':
                curl_bracets_op += 1
            elif lexem.name == '}':
                curl_bracets_cl += 1

        if curl_bracets_cl != curl_bracets_op:
            errors.append()
    
    def _check_syntax(self):
        checked = []
        i = 0
        while i < len(self.lexems):
            last_index = i
            match = True
            for check_list in FOLLOWING_MATRIX:
                for check in check_list:
                    print(check.REGEX, self.lexems[i])
                    if not re.match(check.REGEX, self.lexems[i].name):
                        match = False
                        i = last_index
                        break
                    else:
                        i += 1
                if match:
                    break
            if not match:
                raise SyntaxError(f'Ошибка в строке {self.lexems[i].line}: {self.lexems[i].line_text} -> {self.lexems[i].name} Ошибка синтаксиса')
            i += 1

    def anaylse(self):
        syntaxes = []

        for lexem in self.lexAnalyser.lexems:
            matched = False
            for _class in get_structures():
                new_lexem = _class(lexem[1]+1, self.lexAnalyser._program.lines[lexem[1]], lexem[0].name)
                if re.match(_class.REGEX, lexem[0].name):
                    syntaxes.append(new_lexem)
                    matched = True
            if not matched:
                raise LexError(f'Ошибка в строке {new_lexem.line}: "{new_lexem.line_text}" -> {new_lexem.name} - неопознанная лексема.')

        self.lexems = syntaxes
        # self._find_errors()

        self._check_syntax()
