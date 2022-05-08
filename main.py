# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P2 Parser
# File:        main.py

import os
import sys

from Scanner import LexicalAnalyzer
from Parser import SyntaxAnalyzer


if __name__ == "__main__":
    # DEMO

    # initialize scanner
    scanner = LexicalAnalyzer()
    parser = SyntaxAnalyzer()

    folder = ""

    # initialize test file paths
    test1path = os.path.join(sys.path[0], folder, 'Test1.jl')
    test2path = os.path.join(sys.path[0], folder, 'Test2.jl')
    test3path = os.path.join(sys.path[0], folder, 'Test3.jl')
    modifiedtest1path = os.path.join(sys.path[0], folder, 'modifiedTest1.jl')
    modifiedtest2path = os.path.join(sys.path[0], folder, 'modifiedTest2.jl')
    correctedtest2path = os.path.join(sys.path[0], folder, 'correctedTest2.jl')

    # perform analysis for each test file
    for path_to_run in [test1path, test2path, test3path, modifiedtest1path, modifiedtest2path, correctedtest2path]:
        print()
        head, tail = os.path.split(path_to_run)
        print(tail)
        try:
            scanner.perform_lexical_analysis(path_to_run)
            # # print symbol table
            # print(len(scanner.symbol_table))
            # for idx, line in enumerate(scanner.symbol_table):
            #     print(idx+1, line)
            parser.perform_syntax_analysis(scanner.get_symbol_table(), True)

        except Exception as e:
            print(f"{type(e).__name__}: {e}")
