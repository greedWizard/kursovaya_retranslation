from structures import Program, Lexem, IdentifierKW
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
        bracets = r'(\{|\}|\(|\)|\)|\,|\.)'

        for i in range(len(self._program.lines)):
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

    def anaylse(self):
        syntaxes = []

        for lexem in self.lexAnalyser.lexems:
            matched = False
            for _class in get_structures():
                if re.match(_class.REGEX, lexem[0].name):
                    syntaxes.append(_class(lexem[1], self.lexAnalyser._program.lines[lexem[1]], lexem[0].name))
                    matched = True
            if not matched:
                syntaxes.append(IdentifierKW(lexem[1], self.lexAnalyser._program.lines[lexem[1]], lexem[0].name))
        
        self.syntaxes = syntaxes

        