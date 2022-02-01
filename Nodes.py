from Token import TokenType, Token, RESERVED_KEYWORDS
from Lexer import Lexer

class AST(object):
    pass

#Types of AST (abstract syntax trees) nodes / tipi di nodi AST

class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op: Token, expr: AST):
        self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Boolean(AST):
    def __init__(self, token: Token):
        self.token = token
        if token.value is 'TRUE':
            self.value = True
        else:
            self.value = False


class String(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Compound(AST):
    # Represents a 'BEGIN ... END' block
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.op = op
        self.right = right


class Var(AST):
    # Built only with ID or string tokens
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class ArrayVar(AST):
    # Built using an ARRAY token and an INDEX token
    def __init__(self, token: Token, index: Token):
        self.token = token
        self.value = token.value  # name of array
        self.index = index.value  # index


class Type(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class ArrayType(AST):
    def __init__(self, token: Token, range: Token):
        # Built using a TYPE token and a RANGE token
        self.token = token
        self.value = token.value
        self.range = range.value  # Tuple (min_range, max_range)


class Program(AST):
    def __init__(self, name: str, block: AST):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations: AST, compound_statement: Compound):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):
    def __init__(self, var_node: AST, type_node: AST):
        self.var_node = var_node
        self.type_node = type_node


class Param(AST):
    def __init__(self, var_node: AST, type_node: AST):
        self.var_node = var_node
        self.type_node = type_node


class ProcedureDecl(AST):
    def __init__(self, proc_name, formal_params, block_node: Block):
        self.proc_name = proc_name
        self.formal_params = formal_params  # a list of Param nodes
        self.block_node = block_node


class ProcedureCall(AST):
    def __init__(self, proc_name: str, actual_params: list, token: Token):
        self.proc_name = proc_name
        self.actual_params = actual_params  # a list of AST nodes
        self.token = token
        # a reference to procedure declaration symbol
        self.proc_symbol = None


class FunctionDecl(AST):
    def __init__(self, proc_name: str, formal_params: list, block_node: Block, return_type: Type):
        self.proc_name = proc_name
        self.formal_params = formal_params
        self.block_node = block_node
        self.return_type = return_type



class FunctionCall(AST): #Check for reference to symbol
    def __init__(self, func_name: str, actual_params: list, token: Token):
        self.func_name = func_name
        self.actual_params = actual_params
        self.token = token

        self.func_symbol = None


class Then(AST):
    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child


class Else(AST):
    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child


class Condition(AST):
    def __init__(self, token: Token, condition_node: AST, then_node: AST, else_node: AST):
        self.token = token
        self.condition_node = condition_node
        self.then_node = then_node
        self.else_node = else_node


class Do(AST):
    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child


class While(AST):
    def __init__(self, token: Token, condition_node: AST, do_node: AST):
        self.token = token
        self.condition_node = condition_node
        self.do_node = do_node


class Writeln(AST):
    def __init__(self, token: Token, token_list: list):
        self.token = token
        self.token_list = token_list


class Readln(AST):
    def __init__(self, token: Token, token_list: list):
        self.token = token
        self.token_list = token_list


class NoOp(AST):
    pass
