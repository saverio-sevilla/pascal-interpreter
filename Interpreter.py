from SemanticAnalysis import NodeVisitor
from Parser import *
from Token import *
from Stack import *
from ConstraintDict import CDict


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

        if hasattr(node.type_node, 'range'):
            name = node.var_node.token.value
            ar = self.call_stack.peek()

            min_range = node.type_node.range[0]
            max_range = node.type_node.range[1]
            ar[name] = CDict(min_range, max_range)


    def visit_Type(self, node):
        pass


    def visit_ArrayType(self, node):
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
            if type(token) is tuple:
                ar = self.call_stack.peek()
                var_value = ar.get(token[0].value).get(token[1].value)
                print(var_value, end = "")
            elif token.type is TokenType.STRING:
                print(token.value, end = "")
            elif token.type is TokenType.ID:
                ar = self.call_stack.peek()
                var_value = ar[token.value]
                print(var_value, end = "")

    def visit_Readln(self, node: Readln):
        for token in node.token_list:
            ar = self.call_stack.peek()
            ar[token.value] = input("Enter an input: ")

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

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureDecl(self, node):
        pass

    def visit_ProcedureCall(self, node):
        proc_name = node.proc_name
        proc_symbol = node.proc_symbol

        ar = ActivationRecord(
            name=proc_name,
            type=ARType.PROCEDURE,
            nesting_level=proc_symbol.scope_level + 1,
        )

        formal_params = proc_symbol.formal_params
        actual_params = node.actual_params

        for param_symbol, argument_node in zip(formal_params, actual_params):
            ar[param_symbol.name] = self.visit(argument_node)

        self.call_stack.push(ar)

        self.log(f'ENTER: PROCEDURE {proc_name}')
        self.log(str(self.call_stack))

        # evaluate procedure body
        self.visit(proc_symbol.block_ast)

        self.log(f'LEAVE: PROCEDURE {proc_name}')
        self.log(str(self.call_stack))

        self.call_stack.pop()


    def visit_Assign(self, node):  #Modify for new dict
        if hasattr(node.left, 'index'):
            var_name = node.left.value
            var_value = self.visit(node.right)
            var_index = node.left.index
            ar = self.call_stack.peek()

            #ar[var_name][var_index] = var_value

            ar[var_name].add(var_index, var_value)

        else:
            var_name = node.left.value
            var_value = self.visit(node.right)

            ar = self.call_stack.peek()
            ar[var_name] = var_value

    def visit_Var(self, node):
        var_name = node.value

        ar = self.call_stack.peek()
        var_value = ar.get(var_name)

        return var_value

    def visit_ArrayVar(self, node):
        var_name = node.value
        index = node.index
        ar = self.call_stack.peek()

        #var_value = ar.get(var_name)[index] #Modify

        var_value = ar.get(var_name).get(index)

        return var_value


    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)
