# Pascal interpreter

A simple interpreter for a subset of the Pascal language written in Python, based on the series of Ruslan Spivak, with some extensions. 
The architecture is that of a tree-walk interpreter with separate semantic analysis performed before interpretation.

The features supported include:

- Integers, floats, Booleans and strings
- Assignment, logical, arithmetic and relational operators 
- Conditional statements (if statements and while statements)
- Procedure declarations and calls
- Arrays, limited to declarations and simple assignment, syntax as in Pascal  (Ex. array [2..3] of integer)
- Writeln and readln statements 
- Type checking for non-array type variables 

To be implemented in the future:

- Function calls
- For loops
- Full support for arrays and dynamic arrays, with typechecking
- Pointers
- Records  

