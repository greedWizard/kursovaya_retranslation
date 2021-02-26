import string
import re


class Error(Exception):
    pass


class LexError(Error):
    pass


class SyntaxError(Error):
    pass


class Lexem:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Лексема "{self.name}">'

    def __str__(self):
        return f'<Лексема "{self.name}">'


class ProgramIterator:
    def __init__(self, program):
        self._program = program
        self._index = 0

    def __next__(self):
        if self._index < len(self._program.lines):
            r = self._program.lines[self._index]
            self._index += 1
            return r
        raise StopIteration()


class Program:
    name = ''

    def __init__(self, text : str):
        self.lines = text.split('\n')
        
    def __iter__(self):
        return ProgramIterator(self)

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, i: int):
        return self.lines[i]


class Structure:
    def __init__(self, line : int, line_text: str, name: str = ''):
        self.name = name
        self.line = line
        self.line_text = line_text
    
    def check_syntax(self):
        raise NotImplementedError('Not implemented')

    def __repr__(self):
        return f"<{self.name}>"

    def __str__(self):
        return f"<{self.name}>"


class IdentifierKW(Structure):
    REGEX = r'^[a-z]{1}[0-9]+[a-z]{1}$'

    def __init__(self, line : int, line_text: str, name : str):
        super(IdentifierKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'идентификатор "{self.name}"'


class Operator:
    words = []

    def __init__(self, words):
        self.words = words


class ProgramKW(Structure):
    REGEX = r'program'

    def __init__(self, line : int, line_text: str, name : str):
        super(ProgramKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ключевое слово "{self.name}"'


class VarKW(Structure):
    REGEX = r'var'

    def __init__(self, line : int, line_text: str, name : str):
        super(VarKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ключевое слово "{self.name}"'


class BeginKW(Structure):
    REGEX = r'begin'

    def __init__(self, line : int, line_text: str, name : str):
        super(BeginKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ключевое слово "begin"'


class TypeKW(Structure):
    REGEX = r'(^integer$|^real|^boolean$)'

    def __init__(self, line : int, line_text: str, name : str):
        super(TypeKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'тип {self.name}'


class EndKW(Structure):
    REGEX = r'(^end$)'

    def __init__(self, line : int, line_text: str, name : str):
        super(EndKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ключевое слово "end"'


class IntegerKW(Structure):
    REGEX = r'^\d+$'

    def __init__(self, line : int, line_text: str, name : str):
        super(IntegerKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'целое число {self.name}'


class RealKW(Structure):
    REGEX = r'^\d+\.\d+$'

    def __init__(self, line : int, line_text: str, name : str):
        super(RealKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'дробное число число {self.name}'


class SemiColumnKW(Structure):
    REGEX = r'^;$'

    def __init__(self, line : int, line_text: str, name : str):
        super(SemiColumnKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'точка с запятой'


class AssertionKW(Structure):
    REGEX = r'^ass$'

    def __init__(self, line : int, line_text: str, name : str):
        super(AssertionKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'назначение'


class DotKW(Structure):
    REGEX = r'^\.$'

    def __init__(self, line : int, line_text: str, name : str):
        super(DotKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'точка'


class ReadKW(Structure):
    REGEX = r'^read$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ReadKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ключевое слово read'


class ForKW(Structure):
    REGEX = r'^for$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ForKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ключевое слово for'


class ComaKW(Structure):
    REGEX = r'^\,$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ComaKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'запятая'
    

class CurlBracketCloseKW(Structure):
    REGEX = r'^\}$'

    def __init__(self, line : int, line_text: str, name : str):
        super(CurlBracketCloseKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'закр. фигурная скобка'


class CurlBracketOpenKW(Structure):
    REGEX = r'^\{$'

    def __init__(self, line : int, line_text: str, name : str):
        super(CurlBracketOpenKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'откр. фигурная скобка'


class BracketOpenKW(Structure):
    REGEX = r'^\($'

    def __init__(self, line : int, line_text: str, name : str):
        super(BracketOpenKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'откр. скобка'


class BracketCloseKW(Structure):
    REGEX = r'^\)$'

    def __init__(self, line : int, line_text: str, name : str):
        super(BracketCloseKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'закр. скобка'


class WriteKW(Structure):
    REGEX = r'^writeln$'

    def __init__(self, line : int, line_text: str, name : str):
        super(WriteKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'вывод выражения'



class OperationKW(Structure):
    REGEX = r'^(\-|\+|\*|\/)$'

    def __init__(self, line : int, line_text: str, name : str):
        super(OperationKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'арифм. операция {self.name}'


class ColumnKW(Structure):
    REGEX = r'^\:$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ColumnKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'двоеточие'


FOLLOWING_MATRIX = [
    [
        ProgramKW, VarKW
    ],
    [
        CurlBracketOpenKW, IdentifierKW, CurlBracketOpenKW, ComaKW, IdentifierKW, CurlBracketCloseKW, ColumnKW, TypeKW, SemiColumnKW, CurlBracketCloseKW,
    ],
    [
        BeginKW, CurlBracketOpenKW, SemiColumnKW,
    ],
    [
        ReadKW, BracketOpenKW, IdentifierKW, ComaKW, CurlBracketOpenKW, ComaKW, IdentifierKW, CurlBracketCloseKW, BracketCloseKW,
    ],
    [
        BeginKW, CurlBracketOpenKW, SemiColumnKW
    ],
    [
        IdentifierKW, AssertionKW, IntegerKW,
    ],
    [
        OperationKW, RealKW,
    ],
    # [
    #     CurlBracketOpenKW, CurlBracketCloseKW
    # ],
]