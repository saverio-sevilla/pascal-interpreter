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

### Variables and writeln function

This simple program defines 3 integer values in the VAR section, initializes them in a BEGIN-END block, then prints them to screen using the writeln function.
Both single line comments (which start with //) and comment blocks (which are enclosed in curly braces) can be used. The latter kind can span multiple lines.
Currently the interpreter supports the creating of variables in the VAR section but not their initialization. 

The writeln() function is mostly a wrapper over the Python print statement, it supports the printing of multiple comma separated strings and variables. 

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

the output is:
```
Value of a: 5
Value of b: 10
Value of c: 15
```


