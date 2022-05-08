# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P2 Parser
# File:        Parser.py

from collections import deque

from Helper import GRAMMAR, AnalysisError

class SyntaxAnalyzer:

    def __init__(self) -> None:
        # initialize class
        self.__print = False
        self.__flat_sym_tab: deque = []
        self.__derivation = ""

    def __analyze(self, non_terminal: str = "<program>"):
        q = deque()
        # add to queue to handle if there is only one possible derivation
        if len(GRAMMAR[non_terminal])==1:
            q.extend(GRAMMAR[non_terminal][0])
            definition = " ".join(q)
            if self.__derivation == "":
                self.__derivation = f"{non_terminal} => {definition}"
            else:
                self.__derivation = self.__derivation.replace(non_terminal, definition, 1)
            self.__format_derivation()
        # handle case of multiple options.
        # first, the type is determined
        # if it is a statement, recurses to process the statement type
        # if arithemtic expression, derived down to most granular form directly
        #                           or added to queue and processed partially recursively if using arithmetic_op
        # if relative operator, derived down to most granular form directly
        else:
            next_symbol, next_symbol_line_num = self.__flat_sym_tab[-1]

            # determine statement type and recursively process
            if "<statement>" == non_terminal:
                if next_symbol.token_type == "id":
                    g_s = "<assignment_statement>"
                    self.__derivation = self.__derivation.replace(non_terminal, g_s, 1)
                    self.__format_derivation()
                    self.__analyze(non_terminal="<assignment_statement>")
                elif next_symbol.token_type == "reserved_word":
                    g_s = f"<{next_symbol.lexeme}_statement>"
                    if g_s in GRAMMAR:
                        self.__derivation = self.__derivation.replace(non_terminal, g_s, 1)
                        self.__format_derivation()
                        self.__analyze(non_terminal=g_s)
                        return
                    # not a valid statement per grammar
                    else:
                        raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tInvalid start to statement")
                # not a valid statement per grammar
                else:
                    raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tInvalid start to statement")
            # determine arithmetic expression type and derive
            elif "<arithmetic_expression>" == non_terminal:
                if next_symbol.token_type in ("id", "literal_integer"):
                    self.__flat_sym_tab.pop()
                    self.__derivation = self.__derivation.replace(non_terminal, next_symbol.token_type, 1)
                    self.__format_derivation()
                    return
                # derive operator type
                elif "operator" in next_symbol.token_type:
                    if next_symbol.token_type[:3] in ('add', 'sub', 'mul', 'div'):
                        q.extend(GRAMMAR[non_terminal][2])
                        definition = " ".join(q)
                        self.__derivation = self.__derivation.replace(non_terminal, definition, 1)
                        self.__format_derivation()

                        while len(q)>0:
                            if '<arithmetic_op>' == q[0]:
                                self.__flat_sym_tab.pop()
                                self.__derivation = self.__derivation.replace(q.popleft(), next_symbol.token_type, 1)
                                self.__format_derivation()
                            else:
                                self.__analyze(q.popleft())
                        return
                    # invalid operator
                    else:
                        raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tInvalid operator used.")
                # not a valid part of arithemetic expression as per grammar
                else:
                    raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tNot a valid part of an arithmetic expression.")
            # determine relative op type and derive
            elif "<relative_op>" == non_terminal:
                # derive operator type
                if "operator" in next_symbol.token_type:
                    if next_symbol.token_type[:2] in ('le', 'lt', 'ge', 'gt', 'eq', 'ne'):
                        self.__flat_sym_tab.pop()
                        self.__derivation = self.__derivation.replace(non_terminal, next_symbol.token_type, 1)
                        self.__format_derivation()
                        return
                    # invalid operator
                    else:
                        raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tInvalid operator used.")
                # not an operator
                else:
                    raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tNot a valid part of a boolean expression.")
            # not part of grammar
            else:
                raise AnalysisError(f"Invalid syntax on line {next_symbol_line_num+1}: {next_symbol.lexeme}\n\tUnrecognized grammatical unit")

        # process queue
        while len(q)>0 and len(self.__flat_sym_tab)>0:
            # pop off stack and queue
            current_symbol, symbol_line_num = self.__flat_sym_tab.pop()
            current_grammar_def_snippet = q.popleft()

            # validate lexeme
            if current_grammar_def_snippet == current_symbol.token_type:
                continue
            elif current_symbol.token_type == "reserved_word" and current_grammar_def_snippet == current_symbol.lexeme:
                continue
            # handle case where grammar needs further derviation
            elif "<" in current_grammar_def_snippet:
                self.__flat_sym_tab.append((current_symbol, symbol_line_num))
                # optional block is reached
                if current_grammar_def_snippet == "[<block>]":
                    # if block does not match grammar, ignore and check next grammar unit in queue
                    if (current_symbol.token_type == "reserved_word"
                        and current_symbol.lexeme in ("end", "else", "until")):
                        self.__derivation = self.__derivation.replace(" [<block>]", "", 1)
                        self.__format_derivation()
                        continue
                    # recursively derive optional block where made use of
                    else:
                        current_grammar_def_snippet = current_grammar_def_snippet[1:-1]
                        self.__derivation = self.__derivation.replace("[<block>]", current_grammar_def_snippet, 1)
                self.__analyze(non_terminal=current_grammar_def_snippet)
            # program does not match grammar
            else:
                raise AnalysisError(f"Invalid syntax on line {symbol_line_num+1}: {current_symbol.lexeme}\n\tExpected an \"{current_grammar_def_snippet}\"")

        # empty symbol table but remaining expected syntax in queue
        if len(q)>0:
            raise AnalysisError(f"Invalid syntax. Program termination not written correctly")

        # empty queue but remaining program in symbol table
        if non_terminal == "<program>" and len(self.__flat_sym_tab)>0:
            raise AnalysisError(f"Invalid syntax. Program is longer than expected.")

    def __format_derivation(self):
        self.__derivation = self.__derivation.replace("opening_parenthesis", "(")
        self.__derivation = self.__derivation.replace("closing_parenthesis", ")")
        self.__derivation = self.__derivation.replace(" id ", " <id> ")
        self.__derivation = self.__derivation.replace(" literal_integer", " <literal_integer>")
        self.__derivation = self.__derivation.replace(" assignment_operator", " <assignment_operator>")
        if self.__print:
            print(self.__derivation)

    def __flatten_symbol_table(self, symbol_table: list)->list:
        f_s_t = deque()
        for line_num, line in enumerate(symbol_table):
            for sym in line:
                f_s_t.appendleft((sym, line_num))
        return f_s_t

    def perform_syntax_analysis(self, symbol_table: list, print_process: bool = False):
        self.__print = print_process
        self.__derivation = ""
        self.__flat_sym_tab = self.__flatten_symbol_table(symbol_table)
        print("\nPARSING...\n")
        self.__analyze()
        print("\nPARSING COMPLETE.\n")
        print("Parsing Result:\n", self.__derivation)

    def get_derivation(self):
        return self.__derivation
