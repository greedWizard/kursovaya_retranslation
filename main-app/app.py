from analysers import PreProcessor, Analyser
from structures import Program


test_text = ''

with open('test.program', 'rt') as f:
    test_text = f.read()

program = Program(test_text)
pp = PreProcessor(program)
pp.process()

analyser = Analyser(pp)
analyser.syntax_analyse()
print(analyser.lexems)