from SemanticAnalysis import *
from Parser import Parser
from Lexer import Lexer
from Interpreter import Interpreter
from Token import _build_reserved_keywords



def main():

    text = """

    program Main;

    procedure Alpha(a : integer; b : integer);
    var x : integer;

        procedure Beta(a : integer; b : integer);
        var x : integer;
        begin
            x := a * 10 + b * 2;
        end;

    begin
        x := (a + b ) * 2;

        Beta(5, 10);      { procedure call }
    end;

    begin { Main }

        Alpha(3 + 5, 7);  { procedure call }

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