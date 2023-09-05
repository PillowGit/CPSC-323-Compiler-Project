"""
Written by:
Esteban Escartin
Roman Guillermo

This file contains the code for lexical analysis of a RAT32F source file.

This file is implemented as a module file for ease of use in future project
assignments. 
"""

# A set containing every separator in RAT32F
separators: set = set([ '#', '(', ')', ',', '{', '}', ';'])

# A set containing every keyword in RAT32F
keywords: set = set(['function', 'integer', 'bool', 'real', 'if', 'else', 'endif', 'ret', 'put', 'get', 'while'])

# A set containing every operator in RAT32F
operators: set = set(['=', '==', '!=', '>', '<', '<=', '=>', '+', '-', '*', '/'])


# This is an example of what I think a Lexer for our example input may look like
# This is the example input we are working with:
# while (fahr <= upper) a = 23.00; [* this is a sample *]

class FSM:
    def __init__(self):
        self.symbols: set = {'whitespace', 'chr', 'int', 'dot', 'special', 'separator', 'operator', 'ignore'}
        self.states: set = {'keyword', 'identifier', 'int', 'real', 'operator', 'accepted'}
        

example_input = r'while (fahr <= upper) a = 23.00; [* this is a sample *]'