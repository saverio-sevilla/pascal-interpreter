from SemanticAnalysis import *
from Parser import Parser
from Lexer import Lexer
from Interpreter import Interpreter
from Token import _build_reserved_keywords



def main():

    text = """
    program Main;
    var x, y : integer;
    a : integer;
    arr : array[2..4] of integer;
    begin { Main }
        y := 7;
        a := 12;
        x := (y + 3) * 3;
        arr[2] := 3;
        arr[3] := 8;
        a := a + arr[2];
        writeln(arr[2], "\n" , arr[3], "\n");
        writeln("Hello ", y, "\n");
        writeln(x);
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