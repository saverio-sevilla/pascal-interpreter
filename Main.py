from SemanticAnalysis import *
from Parser import *
from Interpreter import Interpreter
from Token import _build_reserved_keywords

'''
To add: 

ADD LOGGING FUNCTION FOR INTERPRETER
CHECK WHY ERRORS AREN'T SHOWN

Arrays: a: array[1..100] of integer;
        a: array[1..3] of string = ('down', 'the', 'road');

Functions 

Input function: readln(var)

Initial value in var declaration: var
                                    a: integer = 4;
                                    

'''


def main():

    text = """
    program Main;
    var x, y : integer;
    begin { Main }
        y := 7;
        x := (y + 3) * 3;
    end.  { Main }


    """
    RESERVED_KEYWORDS = _build_reserved_keywords()
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



if __name__ == '__main__':
    main()