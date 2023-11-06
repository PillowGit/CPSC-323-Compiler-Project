from lexer import *

qualifiers: set = set(['integer', 'bool', 'real'])

class Syntax():
    def __init__(self, fsm):
        self.token_list = [Token('none', 'filler')]
        self.token_list.extend(fsm.tokens)
        self.curr_index = 0
        self.curr_token = self.token_list[self.curr_index]
        self.switch = True

    def print_token(self, val):
        print(f"Token:{val.state}   Lexeme:{val.token}")
    
    def print_exception(self):
        return f"{self.token_list[self.curr_index + 1].token} at index {self.curr_index}"

    def set_next(self, val='', amt=0):
        if self.switch == True:
            start = self.curr_index
            if val:
                for ind, _ in enumerate(self.token_list[start + 1:]):
                    if self.token_list[start + ind + 1].token == val:
                        self.curr_index = start + ind + amt + 1
                        self.curr_token = self.token_list[self.curr_index]
                        self.print_token(self.curr_token)
                        return self.curr_token
                return EOFError
            self.curr_index = self.curr_index + amt + 1
            self.curr_token = self.token_list[self.curr_index]
            self.print_token(self.curr_token)
            return self.curr_token
        else:
            self.switch = True
            return self.curr_token

    def get_next(self, val='', amt=0):
        start = self.curr_index
        if val:
            for ind, _ in enumerate(self.token_list[start + 1:]):
                if self.token_list[start + ind + 1].state == val or self.token_list[start + ind + 1].token == val:
                    return self.token_list[start + ind + amt + 1]
            return Token('invalid', 'none')

        return self.token_list[start + amt + 1]

    def Rat23F(self, next):
        if self.switch:
            print(
                "<Rat23F> -> <Opt Function Definitions> # <Opt Declaration List> <Statement List> #")

        if self.get_next(val='function').token != 'none':
            self.opt_function_def(self.set_next('function'))
        elif self.get_next().token == 'function':
            self.opt_function_def(self.set_next())

        self.set_next()  # '#'

        if self.get_next().token in qualifiers:
            self.opt_declaration_list(self.set_next())
            self.statement_list(self.set_next())
        elif self.get_next().token != '#':
            self.statement_list(self.set_next())
        self.set_next()  # '#'

    def opt_function_def(self, next):
        if next.token == 'function':
            if self.switch:
                print("<Opt Function Definitions> -> <Function Definitions>")
            self.function_definitions(next)
        else:
            if self.switch:
                print("<Opt Function Definitions> -> ε")
            self.switch = False
            self.empty()

    def function_definitions(self, next):
        if next.token == 'function' and self.get_next(val='function').token == 'none':
            if self.switch:
                print("<Function Definitions -> <Function>")
            self.function(next)
        else:
            if self.switch:
                print("<Function Definitions> -> <Function> <Function Definitions>")
            self.function(next)
            self.function_definitions(self.set_next())

    def function(self, next):
        if next.token == 'function':
            if self.switch:
                print(
                    "<Function> -> function <Identifier> (<Opt Parameter List>) <Opt Declaration List> <Body>")
            if self.get_next().state != 'identifier':
                raise TypeError(f"This token must be an identifier. The token is: " + self.print_exception())
            self.identifier(self.set_next())
            self.set_next()  # '('
            self.opt_parameter_list(self.set_next())
            self.set_next()  # ')'

            if self.get_next().token in qualifiers:
                self.opt_declaration_list(self.set_next())
            self.body(self.set_next())

    def identifier(self, next):
        if self.switch:
            print(f"<Identifier> -> {next.token}")

    def opt_parameter_list(self, next):
        if next.token != ')':
            if self.switch:
                print("<Opt Parameter List> -> <Parameter List>")
            self.parameter_list(next)
        else:
            if self.switch:
                print("<Opt Parameter List> -> ε")
            self.switch = False
            self.empty()

    def parameter_list(self, next):
        if next.state == 'identifier' and (self.get_next(val='keyword', amt=2).state != 'identifier'):
            if self.switch:
                print("<Parameter List> -> <Parameter>")
            self.parameter(next)
        else:
            if self.switch:
                print("<Parameter List> -> <Parameter>, <Parameter List>")
            self.parameter(next)
            self.set_next()  # ','
            self.parameter_list(self.set_next())

    def parameter(self, next):
        if self.switch:
            print("<Parameter> -> <IDs> <Qualifier>")
        if next.state != 'identifier':
            raise TypeError(f"This token must be an identifier. The token is: " + self.print_exception())
        self.IDs(next)
        if self.get_next().token not in qualifiers:
            raise TypeError(f"This token must be a qualifier. The token is: " + self.print_exception())
        self.qualifier(self.set_next())

    def IDs(self, next):
        if self.get_next().token != ',':
            if self.switch:
                print("<IDs> -> <Identifier>")
            self.identifier(next)
        else:
            if self.switch:
                print("<IDs> -> <Identifier>, <IDs>")
            self.identifier(next)
            self.set_next()  # ','
            self.IDs(self.set_next())

    def qualifier(self, next):
        if self.switch:
            print(f"<Qualifier> -> {next.token}")

    def opt_declaration_list(self, next):
        if next.token in qualifiers:
            if self.switch:
                print("<Opt Declaration List> -> <Declaration List>")
            self.declaration_list(next)
        else:
            if self.switch:
                print("<Opt Declaration List> -> ε")
            self.switch = False
            self.empty()

    def declaration_list(self, next):
        if self.get_next(val=';', amt=1).token not in qualifiers:
            if self.switch:
                print("<Declaration List> -> <Declaration>;")
            if next.token not in qualifiers:
                raise TypeError(f"This token must be a qualifier. The token is: " + self.print_exception())
            self.declaration(next)
            self.set_next()  # ';'
        else:
            if self.switch:
                print("<Declaration List> -> <Declaration>; <Declaration List>")
            if next.token not in qualifiers:
                raise TypeError(f"This token must be a qualifier. The token is: " + self.print_exception())
            self.declaration(next)
            self.set_next()  # ';'
            if self.get_next().token not in qualifiers:
                raise TypeError(f"This token must be a qualifier. The token is: " + self.print_exception())
            self.declaration_list(self.set_next())

    def declaration(self, next):
        if self.switch:
            print("<Declaration> -> <Qualifier> <IDs>")
        self.qualifier(next)
        self.IDs(self.set_next())

    def body(self, next):
        if self.switch:
            print("<Body> -> { <Statement List> }")
        if self.get_next().token != '}':
            self.statement_list(self.set_next())
        self.set_next()  # '}'

    def statement_list(self, next):
        if next.token == 'if':
            if (self.get_next(val='endif', amt=1).token == '}' and self.get_next(val=';', amt=1).token == '}') or self.get_next(val='endif', amt=1).token == '#':
                if self.switch:
                    print("<Statement List> -> <Statement>")
                self.statement(next)
            else:
                if self.switch:
                    print("<Statement List> -> <Statement> <Statement List>")
                self.statement(next)
                self.statement_list(self.set_next())
        elif self.get_next(val=';', amt=1).token == '}' or self.get_next(val=';', amt=1).token == '#':
            if self.switch:
                print("<Statement List> -> <Statement>")
            self.statement(next)
        else:
            if self.switch:
                print("<Statement List> -> <Statement> <Statement List>")
            self.statement(next)
            self.statement_list(self.set_next())

    def statement(self, next):
        if next.token == '{':
            if self.switch:
                print("<Statement> -> <Compound>")
            self.compound(next)
        elif next.state == 'identifier':
            if self.switch:
                print("<Statement> -> <Assign>")
            self.assign(next)
        elif next.token == 'if':
            if self.switch:
                print("<Statement> -> <If>")
            self.If(next)
        elif next.token == 'ret':
            if self.switch:
                print("<Statement> -> <Return>")
            self.Return(next)
        elif next.token == 'put':
            if self.switch:
                print("<Statement> -> <Print>")
            self.print(next)
        elif next.token == 'get':
            if self.switch:
                print("<Statement> -> <Scan>")
            self.scan(next)
        elif next.token == 'while':
            if self.switch:
                print("<Statement> -> <While>")
            self.While(next)
        else:
            raise TypeError(f"This token is not acceptable for a statement: " + self.print_exception())

    def compound(self, next):
        if self.switch:
            print("<Compound> -> { <Statement List> }")
        if self.get_next().token != '}':
            self.statement_list(self.set_next())
        self.set_next()  # '}'

    def assign(self, next):
        if self.switch:
            print("<Assign> -> <Identifier> = <Expression>;")
        self.identifier(next)
        self.set_next()  # '='
        self.expression(self.set_next())
        self.set_next()  # ';'

    def If(self, next):
        temp_list = []

        for token in self.token_list[self.curr_index:]:
            temp_list.append(token.token)

        try:
            else_token = temp_list.index('else')
        except:
            else_token = 9999999

        endif_token = temp_list.index('endif')

        if else_token < endif_token:
            if self.switch:
                print("<If> -> if ( <Condition> ) <Statement> else <Statement> endif")
            found = True
        else:
            if self.switch:
                print("<If> -> if ( <Condition> ) <Statement> endif")
            found = False

        self.set_next()  # '('
        self.condition(self.set_next())
        self.set_next()  # ')'
        self.statement(self.set_next())

        if found:
            self.set_next()  # 'else
            self.statement(self.set_next())
            self.set_next()  # 'endif'
        else:
            self.set_next()  # 'endif'

    def Return(self, next):
        if self.get_next().token == ';':
            if self.switch:
                print("<Return> -> ret;")
            self.set_next()  # ';'
        else:
            if self.switch:
                print("<Return> -> ret <Expression>;")
            self.expression(self.set_next())
            self.set_next()  # ';'

    def print(self, next):
        if self.switch:
            print("<Print> -> put ( <Expression> );")
        self.set_next()  # '('
        self.expression(self.set_next())
        self.set_next()  # ')'
        self.set_next()  # ';'

    def scan(self, next):
        if self.switch:
            print("<Scan> -> get ( <IDs> );")
        self.set_next()  # '('
        self.IDs(self.set_next())
        self.set_next()  # ')'
        self.set_next()  # ';'

    def While(self, next):
        if self.switch:
            print("<While> -> while ( <Condition> ) <Statement>")
        self.set_next()  # '('
        self.condition(self.set_next())
        self.set_next()  # ')'
        self.statement(self.set_next())

    def condition(self, next):
        if self.switch:
            print("<Condition> -> <Expression> <Relop> <Expression>")
        self.expression(next)
        self.relop(self.set_next())
        self.expression(self.set_next())

    def relop(self, next):
        if self.switch:
            print(f"<Relop> -> {next.token}")

    def expression(self, next):
        if self.switch:
            print("<Expression> -> <Term> <Expression Prime>")
        self.term(next)
        self.expression2(self.set_next())

    def expression2(self, next):
        if next.token == '+':
            if self.switch:
                print("<Expression Prime> -> + <Term> <Expression Prime>")
            self.term(self.set_next())
            self.expression2(self.set_next())
        elif next.token == '-':
            if self.switch:
                print("<Expression Prime> -> - <Term> <Expression Prime>")
            self.term(self.set_next())
            self.expression2(self.set_next())
        else:
            if self.switch:
                print("<Expression Prime> -> ε")
            self.switch = False
            self.empty()

    def term(self, next):
        if self.switch:
            print("<Term> -> <Factor> <Term Prime>")
        self.factor(next)
        self.term2(self.set_next())

    def term2(self, next):
        if next.token == '*':
            if self.switch:
                print("<Term Prime> -> * <Factor> <Term Prime>")
            self.factor(self.set_next())
            self.term2(self.set_next())
        elif next.token == '/':
            if self.switch:
                print("<Term Prime> -> / <Factor> <Term Prime>")
            self.factor(self.set_next())
            self.term2(self.set_next())
        else:
            if self.switch:
                print("<Term Prime> -> ε")
            self.switch = False
            self.empty()

    def factor(self, next):
        if next.token == '-':
            if self.switch:
                print("<Factor> -> - <Primary>")
            self.primary(self.set_next())
        else:
            if self.switch:
                print("<Factor> -> <Primary>")
            self.primary(next)

    def primary(self, next):
        if next.state == 'identifier' and (next.token != 'true' and next.token != 'false'):
            if self.get_next().token == '(':
                if self.switch:
                    print("<Primary> -> <Identifier> ( <IDs> )")
                self.identifier(next)
                self.set_next()  # '('
                self.IDs(self.set_next())
                self.set_next()  # ')'
            else:
                if self.switch:
                    print("<Primary> -> <Identifier>")
                self.identifier(next)
        elif next.state == 'real':
            if self.switch:
                print("<Primary> -> <Real>")
            self.real(next)
        elif next.state == 'int':
            if self.switch:
                print("<Primary> -> <Integer>")
            self.integer(next)
        elif next.token == '(':
            if self.switch:
                print("<Primary> -> ( <Expression> )")
            self.expression(self.set_next())
            self.set_next()  # ')'
        elif next.token == 'true':
            if self.switch:
                print("<Primary> -> true")
        elif next.token == 'false':
            if self.switch:
                print("<Primary> -> false")
        else:
            raise TypeError(f"This token is not acceptable for a primary: " + self.print_exception())

    def integer(self, next):
        if self.switch:
            print(f"<Integer> -> {next.token}")

    def real(self, next):
        if self.switch:
            print(f"<Real> -> {next.token}")

    def empty(self):
        return
