# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P2 Parser
# File:        Scanner.py

from collections import namedtuple
import re

from Helper import TOKENS, AnalysisError, Symbol, RESERVED_WORDS

class LexicalAnalyzer:

    def __init__(self) -> None:
        # initialize class

        # symbol table, will be list of lists
        # indices of outer list correspond to lines (0 indexed)
        # indices of inner list correspond to lexemes (0 indexed)
        self.__symbol_table: list[list[Symbol]]= []

    def __validate(self, lexical_unit:str) -> str:
        # check whether the unit matches a token
        # returns the token_type if found else returns None

        # iterate through tokens
        for token_type, regex in TOKENS.items():

            # check for exact match of regex
            if re.fullmatch(regex, lexical_unit):

                # check to see if multichar string is a reserved word
                if token_type=='other':
                    if lexical_unit in RESERVED_WORDS:
                        # assign correct token type
                        token_type="reserved_word"
                    else:
                        return None

                return token_type

        return None

    def __insert_into_symbol_table(self, *, line:int, token_type:str, lexical_unit:str) -> None:
        # appends token_type and the lexical unit to the list corresponding to the line
        self.__symbol_table[line].append(Symbol(token_type, lexical_unit))

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
                        # print(self.__symbol_table[index_of_row][-1])
                else:
                    raise AnalysisError(f"Invalid lexical unit on line {index_of_row+1}: {unit}")

    def perform_lexical_analysis(self, path:str) -> None:
        # clear symbol table for new analysis
        self.__symbol_table = []

        # open file
        with open(path) as file:

            # iterate lines of file
            for idx, line in enumerate(file):

                # initialize list for that row
                self.__symbol_table.append([])

                # ignore line if comment
                if line[0] in ('//'):
                    continue

                # split line into list of lexical units
                row = line.split()

                # analyze row's lexical units
                self.__analyze_list(index_of_row=idx, list_of_tokens=row)

    def get_symbol_table(self):
        return self.__symbol_table
