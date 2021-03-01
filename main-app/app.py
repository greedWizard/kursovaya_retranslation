from analysers import PreProcessor, Analyser
from structures import Program, SyntaxError, LexError, SymanticError
import tkinter as tk


class MainApp(tk.Tk):
    def initialize_program(self):
        program_text = self.text_area.get("1.0", tk.END)
        self.program = Program(program_text)
        self.preProcessor = PreProcessor(self.program)
        self.analyser = Analyser(self.preProcessor)

        self.errors.delete(0, tk.END)
        self.lexems.delete(0, tk.END)
        
        try:
            lexems = self.analyser.get_lexems()
        except Exception as e:
            self.errors.insert(0, str(e))
            return
        
        for i in range(len(lexems)):
            self.lexems.insert(i, str(lexems[i]))

        self.syntaxButton.config(state=tk.ACTIVE)

    def syntax_analyse(self):
        self.initialize_program()
        self.errors.delete(0, tk.END)
        try:
            self.analyser.syntax_analyse()
        except Exception as e:
            self.errors.insert(0, str(e))

        self.symanticButton.config(state=tk.ACTIVE)

    def symantic_analyse(self):
        self.errors.delete(0, tk.END)

        try:
            self.analyser.symantic_analyse()
        except SymanticError as e:
            self.errors.insert(0, str(e))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        container = tk.Frame(self)
        self.initialized = False

        self.title('Курсовая Богданёнок Все Права Защищены')

        self.program_text = tk.StringVar()

        tk.Label(container, text='Текст программы:').grid(row=0, column=0, sticky=tk.W)
        
        self.text_area = tk.Text(container, width=50, height=25)

        self.text_area.grid(row=1, column=0)
        container.grid(row=1, column=0, sticky=tk.W)

        lex_button = tk.Button(container, text="Лексический анализ", command=self.initialize_program)
        lex_button.grid(row=2, column=0)

        tk.Label(container, text='Лексемы').grid(row=0, column=1, sticky=tk.W)
        self.lexems = tk.Listbox(container, height=25, width=30)
        self.lexems.grid(row=1, column=1, sticky=tk.N)

        tk.Label(container, text='Возникшие ошибки').grid(row=0, column=2, sticky=tk.W)
        self.errors = tk.Listbox(container, height=25, width=100)
        self.errors.grid(row=1, column=2, sticky=tk.N)

        self.syntaxButton = tk.Button(container, text="Синтаксический анализ", command=self.syntax_analyse)
        self.syntaxButton.config(state=tk.DISABLED)

        self.syntaxButton.grid(column=0, row=4)

        self.symanticButton = tk.Button(container, text="Семантический анализ", command=self.symantic_analyse)
        self.symanticButton.config(state=tk.DISABLED)

        self.symanticButton.grid(column=0, row=5)


test_text = ''

with open('test.program', 'rt') as f:
    test_text = f.read()


main_app = MainApp()

main_app.mainloop()
