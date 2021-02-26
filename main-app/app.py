from analysers import LexAnalyser, SyntaxAnalyzer
from structures import Program


test_text = ''

with open('test.program', 'rt') as f:
    test_text = f.read()

program = Program(test_text)
la = LexAnalyser(program)
la.analyse()

syntaxAnalyser = SyntaxAnalyzer(la)
syntaxAnalyser.anaylse()
