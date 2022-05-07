# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P1 Scanner

from collections import namedtuple
import re

class AnalysisError(Exception):
    pass

class LexicalAnalyzer:

    def __init__(self) -> None:
        # initialize class

        # dictionary of tokens and their regex for checking each lexeme
        # based on list provided in project files
        self.__tokens = {
            "id": r'^[a-zA-Z]{1}$',
            "literal_integer": r'^\d+$',
            "assignment_operator": r'^=$',
            "le_operator": r'^<=$',
            "lt_operator": r'^<$',
            "ge_operator": r'^>=$',
            "gt_operator": r'^>$',
            "eq_operator": r'^==$',
            "ne_operator": r'^~=$',
            "add_operator": r'^\+$',
            "sub_operator": r'^-$',
            "mul_operator": r'^\*$',
            "div_operator": r'^/$',
            "function_call": r'^\w*\(\w*\)$',
            "opening_parenthesis": r'^\($',
            "closing_parenthesis": r'^\)$',
            "other": r'^\w+$',
        }

        # reserved words to be checked if lexeme matches 'other' token
        # list taken from https://docs.julialang.org/en/v1/base/base/#Keywords and added more
        self.__reserved_words = [
            'baremodule', 'begin', 'break', 'catch', 'const', 'continue', 'do', 'else', 'elseif',
            'end', 'export', 'false', 'finally', 'for', 'function', 'global', 'if', 'import', 'let',
            'local', 'macro', 'module', 'quote', 'return', 'struct', 'true', 'try', 'using', 'while',
            # list taken from the grammar provided for the syntax analyzer
            'function', 'end', 'if', 'then', 'else', 'while', 'do', 'repeat' 'until', 'print',
            ]

        # named tuple to facilitate storage in symbol table
        self.Symbol = namedtuple('Symbol', ['token_type', 'lexeme'])

        # symbol table, will be list of lists
        # indices of outer list correspond to lines (0 indexed)
        # indices of inner list correspond to lexemes (0 indexed)
        self.symbol_table = []

    def __validate(self, lexical_unit:str) -> str:
        # check whether the unit matches a token
        # returns the token_type if found else returns None

        # iterate through tokens
        for token_type, regex in self.__tokens.items():

            # check for exact match of regex
            if re.fullmatch(regex, lexical_unit):

                # check to see if multichar string is a reserved word
                if token_type=='other':
                    if lexical_unit in self.__reserved_words:
                        # assign correct token type
                        token_type="reserved_word"
                    else:
                        return None

                return token_type

        return None

    def __insert_into_symbol_table(self, *, line:int, token_type:str, lexical_unit:str) -> None:
        # appends token_type and the lexical unit to the list corresponding to the line
        self.symbol_table[line].append(self.Symbol(token_type, lexical_unit))

    def __analyze_list(self, *, index_of_row:int, list_of_tokens:list)->None:
        # validates each lexical unit
        # adds to symbol table if valid else raises exception
        for unit in list_of_tokens:
            # proceed with validation only if string contains something
            if unit!="":
                token_validated = self.__validate(unit)
                if token_validated:
                    # split if function_call to analyze with recursive call else add to symbol table
                    if token_validated=="function_call":
                        function_call = re.split(r'^(\w*)(\()(.*)(\))$', unit)
                        self.__analyze_list(index_of_row=index_of_row, list_of_tokens=function_call)
                    else:
                        self.__insert_into_symbol_table(line=index_of_row, token_type=token_validated, lexical_unit=unit)

                        # # Optional way to print symbol after each insertion
                        # print(self.symbol_table[index_of_row][-1])
                else:
                    raise AnalysisError(f"Invalid lexical unit on line {index_of_row+1}: {unit}")

    def perform_lexical_analysis(self, path:str) -> None:
        # clear symbol table for new analysis
        self.symbol_table=[]

        # open file
        with open(path) as file:

            # iterate lines of file
            for idx, line in enumerate(file):

                # initialize list for that row
                self.symbol_table.append([])

                # ignore line if comment
                if line[0] in ('//'):
                    continue

                # split line into list of lexical units
                row = line.split()

                # analyze row's lexical units
                self.__analyze_list(index_of_row=idx, list_of_tokens=row)
