# Term:        Spring 2022
# Name:        Abdullah Ehsan
# Project:     Deliverable P3 Interpreter
# File:        Helper.py

from collections import namedtuple

# declaration of custom error type for analysis
class AnalysisError(Exception):
    pass

# declaration of namedtuple to facilitate entries to the symbol table
# can be treated as an object but behaves as a tuple
Symbol = namedtuple('Symbol', ['token_type', 'lexeme', 'line_num'])

# dictionary of tokens and their regex for checking each lexeme
# based on list provided in project files
TOKENS = {
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
# list taken from the grammar provided for the syntax analyzer
RESERVED_WORDS = [
    'function', 'end', 'if', 'then', 'else', 'while', 'do', 'repeat', 'until', 'print',
]

GRAMMAR = {
    "<program>": [
            ["function", "id", "opening_parenthesis", "closing_parenthesis", "<block>", "end"]
        ],
    "<block>": [
            ["<statement>", "[<block>]"]
        ],
    "<statement>": [
            ["<if_statement>"],
            ["<assignment_statement>"],
            ["<while_statement>"],
            ["<print_statement>"],
            ["<if_statement>"]
        ],
    "<if_statement>": [
            ["if", "<boolean_expression>", "then", "<block>", "else", "<block>", "end"]
        ],
    "<while_statement>": [
            ["while", "<boolean_expression>", "do", "<block>", "end"]
        ],
    "<assignment_statement>": [
            ["id", "assignment_operator", "<arithmetic_expression>"]
        ],
    "<repeat_statement>": [
            ["repeat", "<block>", "until", "<boolean_expression>"]
        ],
    "<print_statement>": [
            ["print", "opening_parenthesis", "<arithmetic_expression>" , "closing_parenthesis"]
        ],
    "<boolean_expression>": [
            ["<relative_op>", "<arithmetic_expression>", "<arithmetic_expression>"]
        ],
    "<relative_op>": [
            ["le_operator"],
            ["lt_operator"],
            ["ge_operator"],
            ["gt_operator"],
            ["eq_operator"],
            ["ne_operator"]
        ],
    "<arithmetic_expression>": [
            ["id"],
            ["literal_integer"],
            ["<arithmetic_op>", "<arithmetic_expression>", "<arithmetic_expression>"]
        ],
    "<arithmetic_op>": [
            ["add_operator"],
            ["sub_operator"],
            ["mul_operator"],
            ["div_operator"]
        ],
}