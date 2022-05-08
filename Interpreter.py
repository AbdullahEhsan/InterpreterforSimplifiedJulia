# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P3 Interpreter
# File:        Interpreter.py

from Helper import Symbol


class Interpreter:

    def __init__(self) -> None:
        #list of operators used in python/julia
        self.__ops = ['>=', '>', '<=', '<', '==', '!=', '~=', '+', '-', '*', '/']

        # store symbol table
        self.__sym_tab: list[Symbol] = []

        # store the translated to python program for execution
        self.__python_prog = ""

        # tracking for tranlastion
        self.__last_line = 0
        self.__indent_count = 0

    def is_assignment(self, index:int):
        # check if the id is followed by an '=' i.e. is an assignment statement
        if index+1>=len(self.__sym_tab) or self.__sym_tab[index].token_type != 'id':
            return False
        return (self.__sym_tab[index+1].lexeme == '=')

    def prefix_to_infix(self, start_idx:int):
        # conver boolean expression from prefix notation to infix notation
        prefix = ""
        op_i = start_idx

        while self.__sym_tab[op_i].lexeme in self.__ops \
            or self.__sym_tab[op_i].token_type in ('id', 'literal_integer'):

            # break if id found is beginning of assignment statement
            if self.is_assignment(op_i):
                break

            # convert ne_op to python version
            if self.__sym_tab[op_i].token_type == 'ne_operator':
                prefix += "!= "
            else:
                prefix += f"{self.__sym_tab[op_i].lexeme} "
            op_i += 1

        prefix = prefix.split(" ")

        # convert prefix to infix
        stk = []
        for lx in reversed(prefix):
            if lx == "":
                continue
            if lx in self.__ops:
                partial = f"( {stk.pop()} {lx} {stk.pop()} )"
                stk.append(partial)
            else:
                stk.append(lx)

        op_i -=1
        return (op_i, stk.pop())

    def interpret(self, idx:int, symbol:Symbol):
        # translate symbol(s) to python

        # any extra symbols handled in the function call
        additional_symbols_handled = 0
        # the translation
        block = ""

        if symbol.lexeme == 'function':
            # skip to body of program
            additional_symbols_handled += 3 # id ( )
        else:

            # starts new line to match the julia program
            # since both julia and python rely on white space, it is assumed the julia whitespace is correct
            is_new_line = symbol.line_num != self.__last_line
            if is_new_line:
                block += "\n"
                self.__last_line = symbol.line_num

            # add correct ident to line
            if symbol.token_type in ('reserved_word', 'id') and is_new_line:
                block += "\t"*self.__indent_count

            # repeat-until loop (doesnt exist in actual julia)
            # treated as a do-while loop
            # since python doesn't have a do while loop:
            # handled as infinite while loop that break using an if
            if symbol.lexeme == 'repeat':
                block += "while True:\n"
                self.__indent_count += 1
            elif symbol.lexeme == 'until':
                adtl_syms_count, blk = self.interpret(idx+1, self.__sym_tab[idx+1])
                additional_symbols_handled += 1 + adtl_syms_count
                block += f"if {blk}:\n"
                block += "\t"*(self.__indent_count+1)
                block += "break\n"
                self.__indent_count -= 1

            # boolean expression
            # complete expression handled in function call
            # translated to infix
            elif symbol.lexeme in self.__ops:
                stop_idx, infix = self.prefix_to_infix(idx)

                adtl_syms_idx = idx
                while adtl_syms_idx<stop_idx:
                    additional_symbols_handled += 1
                    adtl_syms_idx += 1
                block += f"{infix} "

            # other special cases that need to be handled
            # add/remove indents and new lines as necessary
            elif symbol.lexeme in ("then", "do"):
                block += ":\n"
                self.__indent_count += 1
            elif symbol.lexeme == "end":
                self.__indent_count -=1
            elif symbol.lexeme == "else":
                block = block[:-1]
                block += "else:\n"
            elif symbol.lexeme == ')':
                block += ")\n"

            # any remaining lexemes should match python syntax so used directly
            else:
                block += f"{symbol.lexeme} "

        return (additional_symbols_handled, block)

    def perform_interpretation(self, symbol_table: "list[Symbol]", print_process: bool = False):
        # re-initialize variables
        self.__indent_count = 0
        self.__python_prog = ""
        self.__sym_tab = symbol_table
        self.__last_line = 0

        # sets up symbol table for translation loop
        symbols = enumerate(iter(self.__sym_tab))
        print("\nINTERPRETING...\n")


        # iterates symbols to translate
        for idx, symbol in symbols:

            # interprets symbol(s) into python
            # writes to program variable
            # if additional symbols were handled, skips them in the loop
            adtl_syms, block = self.interpret(idx, symbol)
            self.__python_prog += block
            while adtl_syms>0:
                adtl_syms -= 1
                next(symbols)

            if print_process:
                print(self.__python_prog,"\n")
        print("\nINTERPRETATION COMPLETE.\n")
        print("Interpretation Result:\n", self.__python_prog)

    def execute_program(self) -> None:
        exec(self.__python_prog)

    def get_interpreted_program(self):
        return self.__python_prog
