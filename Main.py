from SemanticAnalysis import *
from Parser import *
from Interpreter import Interpreter
from Token import _build_reserved_keywords

#Add arrays

def main():

    text = """
    program Main;
    var x, y : integer;
    a : integer;
    arr : array[2..5] of integer;
    idx : array[3] of integer;
    begin { Main }
        y := 7;
        x := (y + 3) * 3;
        readln(y, x);
        writeln("Hello \n");
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