from Nodes import *
from Errors import ErrorCode, ParserError
from Lexer import Lexer
from Token import TokenType
import logging

###############
#   PARSER    #
###############


class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code: ErrorCode, token: Token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type):
        # Compare the token_type with the token found, if matched "eat" the token, else raise error
        if self.current_token.type == token_type:
            logging.debug(f"Token: {token_type}")
            self.current_token = self.lexer.get_next_token()
        else:
            logging.error("Expected token {exp}, found {found}"
                          .format(exp=token_type, found=self.current_token.type))
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

    def declarations(self) -> list:
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

    def procedure_declaration(self) -> ProcedureDecl:
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

    def formal_parameters(self) -> list[Param]:
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

    def formal_parameter_list(self) -> list[Param]:
        """ formal_parameter_list : formal_parameters
                                  | formal_parameters SEMI formal_parameter_list
        """
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

        type_node = self.type_spec()  # Type node or RangeType node
        # This calls the type_spec method to assign the parameter to the right type
        var_declarations = [
            VarDecl(var_node, type_node)  # Types: Var, Type or RangeType
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self) -> Type:
        """type_spec : INTEGER | -> Type
                     | REAL    |
                     | BOOLEAN |
                     | STRING  |
                     | ARRAY    |
        """
        token = self.current_token
        if self.current_token.type in (TokenType.INTEGER, TokenType.REAL, TokenType.BOOL, TokenType.STRING):
            self.eat(self.current_token.type)

        elif self.current_token.type == TokenType.ARRAY:
            self.eat(self.current_token.type)

            if self.current_token.type == TokenType.L_SQ_PAREN:
                self.eat(TokenType.L_SQ_PAREN)
                range_low = self.current_token.value
                self.eat(self.current_token.type)
                while self.current_token.type == TokenType.DOT:
                    self.eat(TokenType.DOT)
                range_high = self.current_token.value
                self.eat(self.current_token.type)
                self.eat(TokenType.R_SQ_PAREN)

            else:
                range_low = 0
                range_high = 0

            self.eat(TokenType.OF)
            if self.current_token.type in (TokenType.INTEGER, TokenType.REAL, TokenType.BOOL, TokenType.STRING):
                token = self.current_token  # Type token
                self.eat(self.current_token.type)
                return RangeType(token, range_low, range_high)
            else:
                logging.error("The type of array elements has not been recognised")

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

    def statement_list(self) -> list[AST]:
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
                  | while_statement
                  | if_statement
                  | writeln_statement
                  | readln_statement
                  | repeat_statement
                  | setlength_statement
                  | empty
        """

        if (self.current_token.type == TokenType.ID
                and self.lexer.current_char == '('):
            node = self.proccall_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.WRITELN:
            node = self.writeln_statement()
        elif self.current_token.type == TokenType.READLN:
            node = self.readln_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.conditional_statement()
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_statement()
        elif self.current_token.type == TokenType.REPEAT:
            node = self.repeat_statement()
        elif self.current_token.type == TokenType.SETLENGTH:
            node = self.set_length_statement()
        else:
            node = self.empty()
        return node

    def proccall_statement(self) -> ProcedureCall:

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


    def set_length_statement(self) -> Setlength:
        token = self.current_token
        self.eat(TokenType.SETLENGTH)
        self.eat(TokenType.LPAREN)
        var_node = self.variable()
        self.eat(TokenType.COMMA)
        length_node = self.expr()
        self.eat(TokenType.RPAREN)

        return Setlength(token=token, var_node=var_node, length_node=length_node)

    def while_statement(self) -> While:
        token = self.current_token
        self.eat(TokenType.WHILE)
        condition_node = self.expr()
        do_node = self.do_statement()

        return While(token=token, condition_node=condition_node, do_node=do_node)

    def repeat_statement(self) -> Repeat:
        token = self.current_token
        self.eat(TokenType.REPEAT)
        repeat_node = self.statement()
        self.eat(TokenType.UNTIL)
        condition_node = self.expr()

        return Repeat(token=token, repeat_node=repeat_node, condition_node=condition_node)

    def do_statement(self) -> Do:
        token = self.current_token
        self.eat(TokenType.DO)
        child = self.statement()
        return Do(token=token, child=child)

    def conditional_statement(self) -> Condition:

        """
        if_statement : IF condition THEN statement (ELSE statement)?
        """

        token = self.current_token
        self.eat(TokenType.IF)
        condition_node = self.expr()
        then_node = self.then_statement()
        else_node = None

        print("Token after if: ", self.current_token.type)
        if self.current_token.type == TokenType.ELSE:
            else_node = self.else_statement()

        return Condition(token=token, condition_node=condition_node, then_node=then_node, else_node=else_node)

    def then_statement(self) -> Then:

        token = self.current_token
        self.eat(TokenType.THEN)
        child = self.statement()
        return Then(token=token, child=child)

    def else_statement(self) -> Else:

        token = self.current_token
        self.eat(TokenType.ELSE)
        child = self.statement()
        return Else(token=token, child=child)

    def writeln_statement(self) -> Writeln:

        node_list = []
        token = self.current_token
        self.eat(TokenType.WRITELN)
        self.eat(TokenType.LPAREN)

        node = self.variable()
        node_list.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.variable()
            node_list.append(node)

        self.eat(TokenType.RPAREN)
        return Writeln(token=token, node_list=node_list)

    def readln_statement(self) -> Readln:
        node_list = []
        token = self.current_token
        self.eat(TokenType.READLN)
        self.eat(TokenType.LPAREN)
        node = self.variable()
        node_list.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.variable()
            node_list.append(node)

        self.eat(TokenType.RPAREN)

        return Readln(token=token, node_list=node_list)

    def assignment_statement(self) -> Assign:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self) -> Var | IndexVar:
        """
        variable : ID
        """

        token = self.current_token

        if self.current_token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
        else:
            self.eat(TokenType.ID)
            if self.current_token.type == TokenType.L_SQ_PAREN:
                self.eat(TokenType.L_SQ_PAREN)
                index = self.expr()
                self.eat(TokenType.R_SQ_PAREN)
                return IndexVar(token, index)

        return Var(token)

    @staticmethod
    def empty() -> AST:
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
            node = BinOp(left=node, op=token, right=self.sixth_priority())

        return node

    def sixth_priority(self) -> AST:
        """
        AND operator
        """
        node = self.fifth_priority()

        while self.current_token.type is TokenType.AND:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.fifth_priority())

        return node

    def fifth_priority(self) -> AST:
        """
        Equality operators =, !=
        """
        node = self.fourth_priority()

        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.fourth_priority())

        return node

    def fourth_priority(self) -> AST:
        """
        Comparison operators >, <, >=, <=
        """
        node = self.third_priority()

        while self.current_token.type in (TokenType.GREATER, TokenType.GREAT_EQ, TokenType.LESSER, TokenType.LESS_EQ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.expr())

        return node

    def third_priority(self) -> AST:
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

    def second_priority(self) -> BinOp:
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

    def first_priority(self) -> UnaryOp | Num | Boolean | String | AST:
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
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            node = self.variable()  # Handles array variables (Ex. arr[5])
            return node

    def parse(self):

        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node
