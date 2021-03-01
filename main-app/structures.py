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
    TYPE = 'keyword'

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
    REGEX = r'^\-?\d+$'
    TYPE = 'variable'

    def __init__(self, line : int, line_text: str, name : str):
        super(IntegerKW, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'целое число {self.name}'


class RealKW(Structure):
    REGEX = r'^\d+\.\d+$'
    TYPE = 'variable'

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
    TYPE = 'bracket'

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
    TYPE = 'bracket'

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
    TYPE = 'keyword'

    def __init__(self, line : int, line_text: str, name : str):
        super(WriteKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'вывод выражения'



class OperationKW(Structure):
    REGEX = r'^(\-|\+|\*|\/)$'
    TYPE = 'operation'

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


class IfKW(Structure):
    REGEX = r'^if$'

    def __init__(self, line : int, line_text: str, name : str):
        super(IfKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово if'


class ThenKW(Structure):
    REGEX = r'^then$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ThenKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово then'


class SqBracketOpenKW(Structure):
    REGEX = r'^\[$'

    def __init__(self, line : int, line_text: str, name : str):
        super(SqBracketOpenKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'^[$'


class SqBracketCloseKW(Structure):
    REGEX = r'^\]$'

    def __init__(self, line : int, line_text: str, name : str):
        super(SqBracketCloseKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f']'


class ElseKW(Structure):
    REGEX = r'^else$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ElseKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово else'


class DoKW(Structure):
    REGEX = r'^do$'

    def __init__(self, line : int, line_text: str, name : str):
        super(DoKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово do'


class LoopKW(Structure):
    REGEX = r'^loop$'

    def __init__(self, line : int, line_text: str, name : str):
        super(LoopKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово loop'


class WhileKW(Structure):
    REGEX = r'^while$'

    def __init__(self, line : int, line_text: str, name : str):
        super(WhileKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово while'


class BooleanKW(Structure):
    REGEX = r'^(true|false)$'

    def __init__(self, line : int, line_text: str, name : str):
        super(BooleanKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово then'


class ComparisonKW(Structure):
    REGEX = r'^(\<|\>|\>\=|\<\=|\=\=|\!\=)$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ComparisonKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'операция сравнения {self.name}'


class ToKW(Structure):
    REGEX = r'^to$'

    def __init__(self, line : int, line_text: str, name : str):
        super(ToKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово to'


class StepKW(Structure):
    REGEX = r'^step$'

    def __init__(self, line : int, line_text: str, name : str):
        super(StepKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово step'


class NextKW(Structure):
    REGEX = r'^next$'

    def __init__(self, line : int, line_text: str, name : str):
        super(NextKW, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'ключевое слово next'


FOLLOWING_MATRIX = [
    [
        CurlBracketOpenKW, IdentifierKW, CurlBracketOpenKW, ComaKW, IdentifierKW, CurlBracketCloseKW, ColumnKW, TypeKW, SemiColumnKW, CurlBracketCloseKW,
    ],
    [
        BeginKW, CurlBracketOpenKW, SemiColumnKW,
    ],
    [
        ProgramKW, VarKW
    ],
    [
        ReadKW, BracketOpenKW, IdentifierKW, ComaKW, CurlBracketOpenKW, ComaKW, IdentifierKW, CurlBracketCloseKW, BracketCloseKW,
    ],
    [
        CurlBracketCloseKW, EndKW, DotKW,
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
    [
        CurlBracketCloseKW, EndKW,
    ],
    [
        IfKW, BooleanKW,
    ],
    [
        ThenKW,
    ],
    [
        SqBracketOpenKW, ElseKW, 
    ],
    [
        SqBracketCloseKW,
    ],
    [
        DoKW, WhileKW, 
    ],
    [
        IntegerKW, ComparisonKW, IntegerKW,
    ],
    [
        RealKW, ComparisonKW, RealKW,
    ],
    [
        LoopKW,
    ],
    [
        CurlBracketOpenKW, ComaKW,
    ],
    [
        CurlBracketCloseKW,
    ],
    [
        ForKW
    ],
    [
        ToKW, 
    ],
    [
        SqBracketOpenKW, StepKW, 
    ],
    [
        SqBracketCloseKW,
    ],
    [
        NextKW,
    ],
    [
        BracketOpenKW, IntegerKW, OperationKW,
    ],
    [
        IntegerKW, BracketCloseKW,
    ],
    [
        BracketOpenKW, RealKW, OperationKW,
    ],
    [
        RealKW, BracketCloseKW,
    ],
    [
        OperationKW, IntegerKW,
    ],
    [
        OperationKW, RealKW,
    ]
]