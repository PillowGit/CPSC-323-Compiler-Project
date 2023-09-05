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
        # A list of all the symbols our fsm may come across
        self.symbols: set = {'whitespace', 'chr', 'int', 'dot', 'special', 'separator', 'operator', 'comment', 'closecomment'}
        # A list of all the possible states for our fsm
        self.states: set = {'keyword', 'identifier', 'int', 'real', 'operator', 'valid', 'invalid', 'ignore'}
        # The fsm should always start in a valid state
        self.starting_state: str = 'valid'
        # A list of all of the acceptable states at the end of the program, Note: All states are accepted besides "invalid" which would be a lexical analysis error. We do not care about syntax, just analyzing smybols during this phase
        self.accepting_states: set = self.states - set({'invalid'})
        # A list to store all the tokens we have analyzed
        self.tokens: list = []
        # Initialize the table of states and transitions
        self.table: dict = {x : dict() for x in self.states}
        self.create_states()

    def create_states(self):
        # Note: This table does NOT include keyword states. A keyword will be identified mid syntax analysis. This will be done by
        # checking if an accepted identifier is in the keyword list
        # Note: We also do NOT include states for 'invalid'. If we recieve an invalid state during lexical analysis, the 
        # compiler should terminate
        del self.table['invalid']
        del self.table['keyword']

        # New states depending on if our state is 'identifier'
        self.table['identifier']['whitespace'] = 'valid'
        self.table['identifier']['chr'] = 'identifier'
        self.table['identifier']['int'] = 'identifier'
        self.table['identifier']['dot'] = 'invalid'
        self.table['identifier']['special'] = 'invalid'
        self.table['identifier']['separator'] = 'valid'
        self.table['identifier']['operator'] = 'operator'
        self.table['identifier']['comment'] = 'ignore'
        self.table['identifier']['closecomment'] = 'invalid'
        # New states depending on if our state is 'int'
        self.table['int']['whitespace'] = 'valid'
        self.table['int']['chr'] = 'invalid'
        self.table['int']['int'] = 'int'
        self.table['int']['dot'] = 'real'
        self.table['int']['special'] = 'invalid'
        self.table['int']['separator'] = 'valid'
        self.table['int']['operator'] = 'operator'
        self.table['int']['comment'] = 'ignore'
        self.table['int']['closecomment'] = 'invalid'
        # New states depending on if our state is 'real'
        self.table['real']['whitespace'] = 'valid'
        self.table['real']['chr'] = 'invalid'
        self.table['real']['int'] = 'real'
        self.table['real']['dot'] = 'invalid'
        self.table['real']['special'] = 'invalid'
        self.table['real']['separator'] = 'valid'
        self.table['real']['operator'] = 'operator'
        self.table['real']['comment'] = 'ignore'
        self.table['real']['closecomment'] = 'invalid'
        # New states depending on if our state is 'operator'
        self.table['operator']['whitespace'] = 'ignore'
        self.table['operator']['chr'] = 'identifier'
        self.table['operator']['int'] = 'int'
        self.table['operator']['dot'] = 'invalid'
        self.table['operator']['special'] = 'invalid'
        self.table['operator']['separator'] = 'valid' # Note: we don't care if we have something like '(x+)', that's a job for syntax analysis
        self.table['operator']['operator'] = 'valid'
        self.table['operator']['comment'] = 'ignore'
        self.table['operator']['closecomment'] = 'invalid'
        # New states depending on if our state is 'valid' 
        self.table['valid']['whitespace'] = 'valid'
        self.table['valid']['chr'] = 'identifier'
        self.table['valid']['int'] = 'int'
        self.table['valid']['dot'] = 'invalid'
        self.table['valid']['special'] = 'invalid'
        self.table['valid']['separator'] = 'valid' # Note: we don't care if we are given a closed seperated before an opening one. That will be handled in syntax analysis 
        self.table['valid']['operator'] = 'operator'
        self.table['valid']['comment'] = 'ignore'
        self.table['valid']['closecomment'] = 'invalid'
        # New states depending on if our state is 'ignore'
        # Every state besides a new comment will be ignored here, so we can do this in 1 line using dict comprehension and a ternary statement
        self.table['ignore'] = {x : 'ignore' if x != 'closecomment' else 'valid' for x in self.symbols}

        self.states: set = {'keyword', 'identifier', 'int', 'real', 'operator', 'valid', 'invalid', 'ignore'}
    
    def analyze(self, file_path: str):
        # Open the file and read/store its contents
        file_contents: str = ''
        with open(file_path, 'r') as f:
            file_contents = f.read()
        # TO DO
        # Do a bunch of analysis on the text and stuff write logic blah blah


# This library is just to see a pretty visual of our FSM when printing, comment out if you don't have it downloaded
# The rich library can be found here: https://github.com/Textualize/rich
from rich import print
test_fsm = FSM()
print(test_fsm.table)