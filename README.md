# Pascal interpreter

## Intro

A simple interpreter for a subset of the Pascal language written in Python, based on Ruslan Spivak's and extended to support many more features. 
Uses a tree-walk interpreter with separate semantic analysis performed before interpretation.

The features supported include:

- Integers, floats, Booleans and strings
- Assignment, logical, arithmetic and relational operators 
- Conditional statements (if statements and while statements)
- Procedures
- Arrays, limited to declarations and simple assignment, syntax as in Pascal  (Ex. array [2..3] of integer)
- Writeln and readln statements 

To be implemented in the future:

- Function calls
- For loops
- Full support for arrays and dynamic arrays, with typechecking
- Records 

## Examples

```
Program Test;
VAR
a, b, c : INTEGER;

BEGIN {Test}
    BEGIN
        a := 5;  // Assigning values to the variables
        b := 10;
        c := 15;
        writeln("Value of a: ", a );
        writeln("Value of b: ", b );
        writeln("Value of c: ", c );
    END;
END. {Test}
```



