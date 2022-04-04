"""

'|': OR
'?': optional


program : PROGRAM variable SEMI block DOT
block : declarations compound_statement
declarations : (VAR (variable_declaration SEMI)+)*
   | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
   | empty
variable_declaration : ID (COMMA ID)* COLON type_spec
formal_params_list : formal_parameters
                   | formal_parameters SEMI formal_parameter_list
formal_parameters : ID (COMMA ID)* COLON type_spec
type_spec : INTEGER, BOOL, STRING, ARRAY
compound_statement : BEGIN statement_list END
statement_list : statement
               | statement SEMI statement_list
statement : compound_statement
          | proccall statement
          | assignment_statement
          | if_statement
          | while_statement
          | write_statement
          | read_statement
          | empty

proccall_statement : ID LPAREN (expr (COMMA expr)*)? RPAREN
assignment_statement : variable ASSIGN expr
if_statement : IF expr THEN statement (ELSE statement)?
while_statement : WHILE expr DO statement
write_statement : WRITELN LPAREN ID (COMMA ID)* RPAREN
empty :

seventh_priority : sixth_priority OR sixth_priority
sixth_priority : fifth_priority  AND fifth_priority
fifth_priority : fourth_priority (( = | != )  fourth_priority )
fourth_priority : third_priority (( < | > | <= | >= ) third_priority)
third_priority : second_priority ((PLUS | MINUS) second_priority)*
second_priority : first_priority ((MUL | INTEGER_DIV | FLOAT_DIV) first_priority)*
first_priority :
       | unary PLUS factor
       | unary MINUS factor
       | TRUE
       | FALSE
       | STRING
       | INTEGER_CONST
       | REAL_CONST
       | LPAREN expr RPAREN
       | variable
variable: ID
"""