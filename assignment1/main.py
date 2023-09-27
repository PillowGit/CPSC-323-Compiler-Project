"""
Written by:
Esteban Escartin
Roman Guillermo
Jericho Montecillo

This file is a driver file to test our lexer.py function 
"""

# Rich is a python module to help us analyze, output, and format
# text when printing to the console. You can install/view the 
# library here: https://github.com/Textualize/rich
# The pip command is: python -m pip install rich
# Alternatively, you can comment out this import as it is not 100% necessary
from rich import print

# FSM is the driver class defined in lexer.py
from lexer import FSM

# We use these get the list of .txt files to analyze and
# clear our output files to avoid clutter
# getcwd -> Get's the current directory of the program
# listdir -> Lists all of the files in a directory
from os import getcwd, listdir, remove

# Helper function to gather all the files ending in '.txt' and not 'ratout.txt'
def gather_txt_files() -> list:
    return list(filter(lambda x: x[-4:] == '.txt' and '_ratout.txt' not in x, [file for file in listdir(getcwd())]))

# Helper function to ask the user for input
def print_input_prompt(valid_files: dict) -> None:
    out: str = 40*'-'+'\nPlease select one of the following choices:\n\n'
    for i, f in valid_files.items():
        out += f'{str(i+1)}. Generate tokens for \'{f}\'\n'
    out += 'r. Re-search the current directory for more text files\n'
    out += 'c. Clear all token output files\n'
    out += 'q. Quit the file program\n'
    print(out)

# Helper function to print out a list of give tokens. This also writes the output to a file
def print_tokens(file_name: str, tokens: list) -> str:
    out: str = f'\n{file_name} returned us the following token list:\n'
    parsed_tokens: str = ''
    for token in tokens:
        parsed_tokens += f'{token}\n'
    print(out + parsed_tokens + f'This will also be written to a file named \'{file_name[:-4] + "_ratout.txt"}\'')
    f = open(file_name[:-4]+'_ratout.txt','w')
    f.write(parsed_tokens)
    f.close()

# Helper function to clear files with 'ratout.txt'
def clear_excess() -> None:
    newline: str = '\n'
    excess: list = list(filter(lambda x: x[-11:] == '_ratout.txt', [file for file in listdir(getcwd())]))
    if not excess:
        print("\nCould not find any token output files to delete\n")
        return
    print(f'\nThis action will remove the following files:\n{"".join([x+newline for x in excess])}')
    if input("Type y to confirm: ").lower() != 'y':
        return
    else:
        for f in excess:
            remove(getcwd()+f'/{f}')

def main() -> None:
    # Initialize a Finite State Machine that we will use to analyze every file
    driver_fsm: FSM = FSM()
    # Gather all of the .txt files in the current directory
    # Note: All our files containing tokens will end in 'ratout.txt'
    # so we ignore those when gathering all files
    txt_file_choices: dict = dict(enumerate(sorted(gather_txt_files())))

    # Initialize a loop to prompt the user for input
    while True:
        # Ask the user for some input
        print_input_prompt(txt_file_choices)

        # Gather the users input
        user_inp: str = input('Your choice: ')

        # Check if user wishes to quit
        if user_inp.lower() == 'q':
            break

        elif user_inp.lower() == 'c':
            clear_excess()

        # Check if user wishes to regenerate file list
        elif user_inp.lower() == 'r':
            txt_file_choices = dict(enumerate(sorted(gather_txt_files())))

        # Check if the user wants to analyze a file
        elif user_inp.isnumeric() and int(user_inp)-1 in range(len(txt_file_choices)):
            # Ask the FSM to analyze our file 
            driver_fsm.analyze(txt_file_choices[int(user_inp)-1])
            # Hold the tokens that the FSM generates
            token_list: list = driver_fsm.dump_tokens()
            # Print out our tokens
            print_tokens(txt_file_choices[int(user_inp)-1], token_list)
        else:
            print('Invalid input, please try again')



if __name__ == '__main__':
    main()