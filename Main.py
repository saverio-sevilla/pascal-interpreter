from SPI import execute

# Add typechecking

def main():

    text = """

    PROGRAM Part10;
    VAR
    number, int     : INTEGER;
    a, b, c, x : INTEGER;
    y          : REAL;
    arr        : ARRAY [2..10] OF INTEGER;

    BEGIN {Part10}
        BEGIN
            number := 2;
            int := 5.5; {Typechecking???}
            a := number;
            b := 10 * a + 10 * number DIV 4;
            c := a - - b;
            arr[a] := 3;
    END;
    x := 11;
    y := 20 / 7 + 3.14;
   {writeln('a = ', a);}
END.  {Part10}
    """

    execute(text)

if __name__ == '__main__':
    main()

