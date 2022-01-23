from Token import *
from Lexer import Lexer
from Nodes import *
from Errors import Error, ErrorCode, LexerError, SemanticError, ParserError


###############
#   PARSER    #
###############


class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type):
        # Compare the token_type with the token found, if matched "eat" the token, else raise error
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print(token_type)
            print(self.current_token.type)
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )

    def program(self) -> Program:
        """A program starts with the keyword PROGRAM followed by
        the program_name, ';' semicolon, and a BLOCK
        It ends with a DOT '.'
         """
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(TokenType.SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(TokenType.DOT)
        return program_node

    def block(self) -> Block:
        """ Block :
        # declarations
        # compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node


    def declarations(self):
        """
        declarations : (VAR (variable_declaration SEMI)+)? procedure_declaration*
        """
        declarations = []

        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMI)

        while self.current_token.type == TokenType.PROCEDURE:
            proc_decl = self.procedure_declaration()
            declarations.append(proc_decl)

        return declarations

    def procedure_declaration(self):
        """procedure_declaration :
             PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI
        """
        self.eat(TokenType.PROCEDURE)
        proc_name = self.current_token.value
        self.eat(TokenType.ID)
        params = []

        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            params = self.formal_parameter_list()
            self.eat(TokenType.RPAREN)

        self.eat(TokenType.SEMI)
        block_node = self.block()
        proc_decl = ProcedureDecl(proc_name, params, block_node)
        self.eat(TokenType.SEMI)
        return proc_decl


    def formal_parameters(self) -> list:
        """ formal_parameters : ID (COMMA ID)* COLON type_spec """
        param_nodes = []

        param_tokens = [self.current_token]
        self.eat(TokenType.ID)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            param_tokens.append(self.current_token)
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()
        # This calls the type_spec method to assign the parameter to the right type

        for param_token in param_tokens:
            param_node = Param(Var(param_token), type_node)
            param_nodes.append(param_node)

        return param_nodes


    def formal_parameter_list(self) -> list:
        """ formal_parameter_list : formal_parameters
                                  | formal_parameters SEMI formal_parameter_list
        """
        # procedure Foo();
        if not self.current_token.type == TokenType.ID:
            return []

        param_nodes = self.formal_parameters()

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            param_nodes.extend(self.formal_parameters())

        return param_nodes


    def variable_declaration(self) -> list:
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]  # first ID
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()
        # This calls the type_spec method to assign the parameter to the right type
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self): ########## CHECK!
        """type_spec : INTEGER
                     | REAL
                     | BOOLEAN
                     | STRING
        """
        token = self.current_token
        if self.current_token.type in (TokenType.INTEGER, TokenType.REAL, TokenType.BOOL, TokenType.STRING):
            self.eat(self.current_token.type)
        return Type(token)


    def compound_statement(self) -> Compound:
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self) -> list:
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        return results

    def statement(self) -> AST:
        """
        statement : compound_statement
                  | assignment_statement
                  | conditional_statement
                  | empty

        print statements would be added here

        """

        if (self.current_token.type == TokenType.ID and
                self.lexer.current_char == '('
        ):
            node = self.proccall_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.WRITELN:
            node = self.writeln_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.conditional_statement()
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_statement()
        else:
            node = self.empty()
        return node


    def proccall_statement(self):
        """proccall_statement : ID LPAREN (expr (COMMA expr)*)? RPAREN"""
        token = self.current_token

        proc_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        actual_params = []
        if self.current_token.type != TokenType.RPAREN:
            node = self.expr()
            actual_params.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.expr()
            actual_params.append(node)

        self.eat(TokenType.RPAREN)

        node = ProcedureCall(
            proc_name=proc_name,
            actual_params=actual_params,
            token=token,
        )
        return node

    def while_statement(self):
        token = self.current_token
        self.eat(TokenType.WHILE)
        condition_node = self.expr()
        do_node = self.do_statement()

        return While(token=token, condition_node = condition_node, do_node = do_node)


    def do_statement(self):
        token = self.current_token
        self.eat(TokenType.DO)
        child = self.statement()
        return Do(token=token, child=child)


    def conditional_statement(self):
        """
        if-then-else type statement
        """
        token = self.current_token
        self.eat(TokenType.IF)
        condition_node = self.expr()
        then_node = self.then_statement()
        else_node = None

        if self.current_token.type == TokenType.ELSE:
            else_node = self.else_statement()

        return Condition(token=token, condition_node = condition_node, then_node= then_node, else_node=else_node)

    def then_statement(self):
        """
        then_statement: statement that follows an IF statement
        """
        token = self.current_token
        self.eat(TokenType.THEN)
        child = self.statement()
        return Then(token=token, child=child)

    def else_statement(self):
        """
        else_statement: optionally follows an IF statement
        """
        token = self.current_token
        self.eat(TokenType.ELSE)
        child = self.statement()
        return Else(token=token, child=child)


    def writeln_statement(self): #To finish
        token = self.current_token
        token_list = []
        self.eat(TokenType.WRITELN)
        self.eat(TokenType.LPAREN)
        if self.current_token.type == TokenType.STRING:
            token_list.append(self.current_token)
            self.eat(TokenType.STRING)
        else:
            token_list.append(self.current_token)
            self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)

            if self.current_token.type == TokenType.STRING:
                token_list.append(self.current_token)
                self.eat(TokenType.STRING)
            else:
                token_list.append(self.current_token)
                self.eat(TokenType.ID)
        self.eat(TokenType.RPAREN)

        return Writeln(token=token, token_list=token_list)


    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        if self.current_token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
        else:
            self.eat(TokenType.ID)
        return node


    def empty(self):
        return NoOp()

########################################
#  Mathematical and logical operators  #
########################################

    def expr(self) -> AST:
        return self.seventh_priority()

    def seventh_priority(self) -> AST:
        """
        OR operator
        """
        node = self.sixth_priority()

        while self.current_token.type is TokenType.OR:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right = self.sixth_priority())

        return node

    def sixth_priority(self) -> AST:
        """
        AND operator
        """
        node = self.fifth_priority()

        while self.current_token.type is TokenType.AND:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right = self.fifth_priority())

        return node

    def fifth_priority(self) -> AST:
        """
        Equal operators (=, !=)
        """
        node = self.fourth_priority()

        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right = self.fourth_priority())

        return node

    def fourth_priority(self) -> AST:
        """
        Comparison operators (>, <, >=, <=)
        """
        node = self.third_priority()

        while self.current_token.type in (TokenType.GREATER, TokenType.GREAT_EQ, TokenType.LESSER, TokenType.LESS_EQ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right = self.expr())

        return node


    def third_priority(self):
        """
        Operators: PLUS, MINUS
        """
        node = self.second_priority()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.second_priority())

        return node

    def second_priority(self):
        """Operators: MULT, DIV, INTEGER_DIV"""
        node = self.first_priority()

        while self.current_token.type in (TokenType.MUL, TokenType.INTEGER_DIV, TokenType.FLOAT_DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif token.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)

            node = BinOp(left=node, op=token, right=self.first_priority())

        return node

    def first_priority(self):
        '''
        Unary op: PLUS, MINUS, NOT, PARENTHESIS, also returns NUM and BOOL tokens
        '''
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.first_priority())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.first_priority())
            return node
        elif token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            node = UnaryOp(token, self.first_priority())
            return node
        elif token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)
        elif token.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(token)
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(token)

        ##########################
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        """

        '|': OR
        '?': optional
        program : PROGRAM variable SEMI block DOT
        block : declarations compound_statement
        declarations : (VAR (variable_declaration SEMI)+)*
           | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
           | empty
        variable_declaration : ID (COMMA ID)* COLON type_spec
        formal_params_list : formal_parameters
                           | formal_parameters SEMI formal_parameter_list
        formal_parameters : ID (COMMA ID)* COLON type_spec
        type_spec : INTEGER
        compound_statement : BEGIN statement_list END
        statement_list : statement
                       | statement SEMI statement_list
        statement : compound_statement
                  | assignment_statement
                  | empty
        assignment_statement : variable ASSIGN expr
        empty :
        expr : term ((PLUS | MINUS) term)*
        term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        factor : PLUS factor
               | MINUS factor
               | INTEGER_CONST
               | REAL_CONST
               | LPAREN expr RPAREN
               | variable
        variable: ID
        """
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node

