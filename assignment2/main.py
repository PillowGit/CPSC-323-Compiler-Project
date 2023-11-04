"""
Written by:
Esteban Escartin
Jericho Mentecillo
"""



# Rich is a python module to help us analyze, output, and format
# text when printing to the console. You can install/view the
# library here : https://github.com/Textualize/rich
# The pip command is: python -m pip install rich
# Not installing rich will not hinder the SA process
try:
    from rich import print
except Exception as e:
    print("rich was not installed. Console output will not be formatted")

# Syntax is the name for our syntax analyzer
# Our syntax analyzer is written as a Recursive Descent Parser
from syntax import Syntax
from lexer import FSM

# We use a combination of these commands to get the .txt files in 
# the current working directory so that we may clear and create 
# output files seamlessly
from os import getcwd, listdir, remove
from io import StringIO
import sys
import re

# Helper functions to swap stdout process
output_stream: StringIO = StringIO()
def store_stdout() -> None:
    global output_stream
    sys.stdout = output_stream = StringIO()
def restore_stdout() -> None:
    sys.stdout = sys.__stdout__

def get_txt_files() -> list:
    return list(filter(lambda x: x[-4:] == '.txt' and '_SA_out.txt' not in x, [file for file in listdir(getcwd())]))

def print_input_prompt(valid_files: dict) -> None:
    out: str = 40*'-'+'\nPlease select one of the following choices:\n\n'
    for i, f in valid_files.items():
        out += f'{str(i+1)}. Generate Syntax Analysis for \'{f}\'\n'
    out += 'r. Re-search the current directory for more text files\n'
    out += 'c. Clear all SA output files\n'
    out += 'q. Quit the file program\n'
    print(out)

def clear_excess() -> None:
    newline: str = '\n'
    excess: list = list(filter(lambda x: x[-11:] == '_SA_out.txt', [file for file in listdir(getcwd())]))
    if not excess:
        print("\nCould not find any SA output files to delete\n")
        return
    print(f'\nThis action will remove the following files:\n{"".join([x+newline for x in excess])}')
    if input("Type y to confirm: ").lower() != 'y':
        return
    else:
        for f in excess:
            remove(getcwd()+f'/{f}')
            
def run_SA(filepath: str) -> str:
    fsm: FSM = FSM(filename=filepath)
    store_stdout()
    rdp: Syntax = Syntax(fsm=fsm)
    rdp.Rat23F(rdp.token_list[0])
    sa_output: str = output_stream.getvalue()
    restore_stdout()
    ansi_escape = re.compile(r'\x1b[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', sa_output)

def main() -> None:
    txt_file_choices: dict = dict(enumerate(sorted(get_txt_files())))
    while True:
        print_input_prompt(txt_file_choices)
        user_inp: str = input('Your choice: ')
        if user_inp.lower() == 'q':
            break

        elif user_inp.lower() == 'c':
            clear_excess()

        # Check if user wishes to regenerate file list
        elif user_inp.lower() == 'r':
            txt_file_choices = dict(enumerate(sorted(get_txt_files())))

        # Check if the user wants to analyze a file
        elif user_inp.isnumeric() and int(user_inp)-1 in range(len(txt_file_choices)):
            # Ask the FSM to analyze our file 
            file_choice = txt_file_choices[int(user_inp)-1]
            output: str = run_SA(filepath=file_choice)
            # Print out our tokens
            print(output)
            print(f'This will also be written to a file named \'{file_choice[:-4] + "_SA_out.txt"}\'')
            f = open(file_choice[:-4] + "_SA_out.txt", 'w')
            f.write(output)
            f.close()
        else:
            print('Invalid input, please try again')


if __name__ == '__main__':
    main()