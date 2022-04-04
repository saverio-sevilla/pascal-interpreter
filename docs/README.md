# Pascal interpreter

## Intro

A simple interpreter for a subset of the Pascal language written in Python, based on Ruslan Spivak's and extended to support many more features. 
Uses a tree-walk interpreter with separate semantic analysis performed before interpretation.

The features supported include:

- Integers, floats, Booleans and strings
- Assignment, logical, arithmetic and relational operators 
- Conditional statements (if statements and while statements)
- Procedures
- Arrays
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

Variable names can be upper or lower case, must start with a letter or '\_' and must be unique. 

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
### Strings

The interpreter supports basic strings and string assignment.
```
Program Test;
VAR
a : INTEGER;
str1, str2 : STRING;

BEGIN {Test}
    BEGIN
        str1 := "Hello world";
        writeln("str1: ", str1 );
        str2 := str1;
        writeln("str2: " ,str2);
    END;
END. {Test}
```
The program above produces as output, predictably:
```
str1: Hello world
str2: Hello world
```
### Readln and floating point numbers
The readln function accept one variable as parameter and prompts the user to enter a value, which is stores inside the value. 
This program will prompt the user to enter a float and subsequently print it using writeln. 

```
Program Test;
VAR
a, b, c : REAL;

BEGIN {Test}
    BEGIN
        a := 2.2;
        b := 3.14;
        writeln("Enter a float: ");
        readln(c);
        writeln("c: ", c);
    END;
END. {Test}
```

### Loops and conditionals

This simple program shows the use of looping and conditional statements with this interpreter, currently it supports if-else statements, while statements and do-repeat statements. 
A particularity in the syntax is that the BEGIN-END block following an IF statement has a semicolon only at the end of the last block. So a complete if-else statement will have a semicolon at the end of the second block. This is so the parser can differentiate between IF and IF-ELSE statements.

```
Program Test;
VAR
a, b, c : REAL;
BEGIN {Test}
    BEGIN
        a := 5;
        b := 5;
        c := 10;
        WHILE(c > 1)
        DO
            BEGIN
                writeln(c);
                c := c - 1;
            END;

        IF (c = 0)
        THEN
            BEGIN
                writeln("c is zero");
            END
        ELSE
            BEGIN
                writeln("c is not zero");
            END;
    END;
END. {Test}
```

The above program will print the value of c from 10 until 1 is reached, the while loop condition will then be false and the program will just to the correct conditional statement, in this case the ELSE branch, printing "c is not zero". 

### Static Arrays 

The following program will create an array of integer types and fill it with some values in with a while loop. The values are then printed to the screen (in this case the squares from 0 to 100). Note that static arrays declared with the syntax 'ARRAY [i..j] OF (type)' should not be resized with the 'setlength()' function. 

```
Program Test;
VAR
a, b, c : REAL;
arr : ARRAY [0..10] OF INTEGER;
BEGIN {Test}
    BEGIN
        a := 0;
        WHILE (a <= 10)
        DO
        BEGIN
            arr[a] := a * a;
            writeln("The value of arr[",a, "] is: " , arr[a]);
            a := a + 1;
        END;
    END;
END. {Test}
```

### Dynamic arrays 

The interpreter supports basic dynamic arrays created as 'ARRAY OF (type)' and initialized at runtime with 'setlength(array_name, length)'
The method 'setlength' can be called more than once on the same array but may lead to memory leaks. 
```
Program Test;
VAR
i: INTEGER;
dyn_arr : ARRAY OF INTEGER;
BEGIN {Test}
    BEGIN
        i := 0;
        setlength(dyn_arr, 10);
        WHILE (i <= 10)
        DO
        BEGIN
            dyn_arr[i] := i * i * i;
            writeln("The value of dyn_arr[",i, "] is: " , dyn_arr[i]);
            i := i + 1;
        END;
    END;
END. {Test}
```
