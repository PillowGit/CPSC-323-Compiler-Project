### PUSHI {int}
Pushes the int to the top of the stack
### PUSHM {mem}
Pushes the memory location *mem* to the top of the stack
### POPM {mem}
Pops something off the top off the stack, stores it in the *mem* location
### STDOUT 
Pops value from top of stack off, prints it
### STDIN 
Get a users input, put it on top of the stack
### ADD
Pop two values off the stack, add them together, puts result on top of stack
### SUB 
Pops two values off stack, subtracts them (2nd pop - 1st pop), and places the result onto the stack
### MUL
Pops two values off stack, multiplies them, puts result on top of stack
### DIV
Pops two values off stack, divides them (2nd pop - 1st pop), and places the result onto the stack (ignores remainder)
### GRT
Pops two items from the stack. if (2nd pop } 1st pop), pushes 1 to top of stack, else pushes 0
### LES
Pops two items from the stack. if (2nd pop { 1st pop), pushes 1 to top of stack, else pushes 0
### EQU
Pops two items from the stack. If (2nd pop == 1st pop), pushes 1 to top of stack, else pushes 0
### NEQ
Pops two items from the stack. if (2nd pop != 1st pop), pushes 1 to stop of stack, else pushes 0
### GEQ
Pops two items from the stack. if (2nd pop }= 1st pop), pushes 1 to top of stack, else pushes 0
### LEQ
Pops two items from the stack. if (2nd pop {= 1st pop), pushes 1 to top of stack, else pushes 0
### JUMPZ {loc}
Pops an item off the stack. if the value is 0, jump to the loc *loc* specified.
### JUMP {loc}
Jump to the line of code *loc* specified
### LABEL
Empty instruction, defines a spot that can be jumped to in code