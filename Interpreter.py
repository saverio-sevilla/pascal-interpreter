from SemanticAnalysis import NodeVisitor
from Parser import *
from Token import *
from Stack import *


###################
#  INTERPRETER    #
###################


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = CallStack()

    ''' GLOBAL_MEMORY (dictionary) stores the values of the variables declared in the program

    GLOBAL_MEMORY (dizionario) contiene i valori di tutte le variabili dichiarate nel programma
    Serve fino a quando non sara' implementato l'IO

    Interpreter visit functions for AST nodes
    Funzioni di visita per i nodi AST
    '''

    def visit_Program(self, node):
        program_name = node.name
        self.log(f'ENTER: PROGRAM {program_name}')

        ar = ActivationRecord(
            name=program_name,
            type=ARType.PROGRAM,
            nesting_level=1,
        )
        self.call_stack.push(ar)

        self.log(str(self.call_stack))

        self.visit(node.block)

        self.log(f'LEAVE: PROGRAM {program_name}')
        self.log(str(self.call_stack))

        self.call_stack.pop()

    def log(self, msg):
            print(msg)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        # Do nothing
        pass

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == TokenType.FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))
        elif node.op.type == TokenType.AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == TokenType.OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.type == TokenType.EQUAL:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == TokenType.NOT_EQ:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == TokenType.LESSER:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == TokenType.GREATER:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == TokenType.LESS_EQ:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == TokenType.GREAT_EQ:
            return self.visit(node.left) >= self.visit(node.right)


    def visit_Num(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TokenType.PLUS:
            return +self.visit(node.expr)
        elif op == TokenType.MINUS:
            return -self.visit(node.expr)
        elif op == TokenType.NOT:
            return not self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Writeln(self, node: Writeln):
        for token in node.token_list:
            if token.type is TokenType.STRING:
                print(token.value, end = "")
            elif token.type is TokenType.ID:
                print(self.GLOBAL_MEMORY.get(token.value), end = "")

    def visit_Condition(self, node: Condition):
        if self.visit(node.condition_node) is True:
            self.visit(node.then_node)
        elif node.else_node is not None:
            self.visit(node.else_node)

    def visit_While(self, node: While):
        while self.visit(node.condition_node) is True:
            self.visit(node.do_node)

    def visit_Do(self, node: Do):
        self.visit(node.child)

    def visit_Then(self, node: Then):
        self.visit(node.child)

    def visit_Else(self, node: Else):
        self.visit(node.child)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)

        ar = self.call_stack.peek()
        ar[var_name] = var_value

    def visit_Var(self, node):
        var_name = node.value

        ar = self.call_stack.peek()
        var_value = ar.get(var_name)

        return var_value

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureDecl(self, node):
        pass

    def visit_ProcedureCall(self, node):
        pass


    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)