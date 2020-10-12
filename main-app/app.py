from analysers import LexicalAnalyser
from structures import Program


test_text = ''

with open('test.program', 'rt') as f:
    test_text = f.read()

program = Program(test_text)
la = LexicalAnalyser(program)
la.start()

for _ in la.rec_compos:
    print(str(_))