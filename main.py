# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P3 Interpreter
# File:        main.py

import os
import sys

from Scanner import LexicalAnalyzer
from Parser import SyntaxAnalyzer
from Interpreter import Interpreter


if __name__ == "__main__":
    # DEMO

    # initialize scanner
    scanner = LexicalAnalyzer()
    parser = SyntaxAnalyzer()
    interpreter = Interpreter()

    folder = "julia_files"

    # initialize test file paths
    test1path = os.path.join(sys.path[0], folder, 'Test1.jl')
    test2path = os.path.join(sys.path[0], folder, 'Test2.jl')
    test3path = os.path.join(sys.path[0], folder, 'Test3.jl')
    modifiedtest1path = os.path.join(sys.path[0], folder, 'modifiedTest1.jl')
    modifiedtest2path = os.path.join(sys.path[0], folder, 'modifiedTest2.jl')
    correctedtest2path = os.path.join(sys.path[0], folder, 'correctedTest2.jl')
    repeattest = os.path.join(sys.path[0], folder, 'repeatTest.jl')

    # perform analysis for each test file
    for path_to_run in [test1path, test2path, test3path, modifiedtest1path, modifiedtest2path, correctedtest2path, repeattest]:
        print()
        head, tail = os.path.split(path_to_run)
        print(tail)
        print("--------------")
        try:
            scanner.perform_lexical_analysis(path_to_run)
            # print symbol table
            # line = 0
            # for sym in scanner.get_symbol_table():
            #     if sym.line_num == line:
            #         print(sym, end=" ")
            #     else:
            #         line = sym.line_num
            #         print()
            #         print()
            #         print(line, sym, end=" ")
            # print()

            parser.perform_syntax_analysis(scanner.get_symbol_table(), False)

            print("--------------")
            print()

            interpreter.perform_interpretation(scanner.get_symbol_table())

            print("--------------")
            print()

            print('RESULT OF EXECUTION:')
            interpreter.execute_program()

            print("--------------")
            print("--------------")

            print()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
