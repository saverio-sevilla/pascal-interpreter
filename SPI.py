from SemanticAnalysis import *
from Parser import Parser
from Lexer import Lexer
from Interpreter import Interpreter


def build(text):

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    semantic_analyzer = SemanticAnalyzer()

    try:
        semantic_analyzer.visit(tree)

    except Exception as e:
        print(e)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()
