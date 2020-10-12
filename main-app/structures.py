import string
import re


class LexException(Exception):
    pass


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


class Identifier(Structure):
    def __init__(self, line : int, line_text: str, name : str):
        super(Identifier, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'идентификатор "{self.name}"'


class ProgramBegin(Structure):
    def __init__(self, line : int, line_text: str, name : str):
        super(ProgramBegin, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'начало программы с описанием "{self.name}"'


class Type(Structure):
    def __init__(self, line : int, line_text: str, name : str):
        super(Type, self).__init__(line, line_text, name)

    def __repr__(self):
        return f'тип {self.name}'


class EndProgram(Structure):
    def __init__(self, line : int, line_text: str, name : str):
        super(EndProgram, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'окончание программы'


class Read(Structure):
    def __init__(self, line : int, line_text: str, name : str):
        super(Read, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'ввод'


class Declare(Structure):
    def __init__(self, line : int, line_text: str, name : str):
        super(Declare, self).__init__(line, line_text, name)
    
    def __repr__(self):
        return f'объявление переменной'