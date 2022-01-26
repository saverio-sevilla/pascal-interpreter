# Token types / tipologie di Token

from enum import Enum

class Token(object):
    def __init__(self, type, value, lineno = None, column = None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):

        # Printing function for objects of Token type
        # Funzione per stampare oggetti di tipo Token

        return 'Token({type}, {value}), line number: {lineno}'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno
        )

    def __repr__(self):
        return self.__str__()


class TokenType(Enum):
    # single-character token types
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    LPAREN = '('
    RPAREN = ')'
    L_SQ_PAREN = '['
    R_SQ_PAREN = ']'
    EQUAL = '='
    GREATER = '>'
    LESSER = '<'
    GREAT_EQ = '>='
    LESS_EQ = '<='
    NOT_EQ = '=='
    SEMI = ';'
    DOT = '.'
    COLON = ':'
    QUOTE = '"'
    S_QUOTE ='\''
    COMMA = ','
    #Reserved keywords
    PROGRAM = 'PROGRAM'
    ARRAY = 'ARRAY'
    OF = 'OF'
    RANGE = 'RANGE'
    INDEX = 'INDEX'
    INTEGER = 'INTEGER'  # Used for the types INT and REAL
    REAL = 'REAL'
    STRING = 'STRING'
    BOOL = 'BOOL'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    INTEGER_DIV = 'DIV'
    NOT = 'NOT'
    AND = 'AND'
    OR = 'OR'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    BEGIN = 'BEGIN'
    VAR = 'VAR'
    PROCEDURE = 'PROCEDURE'
    WRITELN = 'WRITELN'
    READLN = 'READLN'
    WHILE = 'WHILE'
    DO = 'DO'
    END = 'END'
    EOF = 'EOF'
    # Other keywords
    ASSIGN = ':='
    INTEGER_CONST = 'INTEGER_CONST'  # Values of types INT and REAL
    REAL_CONST = 'REAL_CONST'
    ID = 'ID'


"""
List of reserved keywords
The list must necessarily include only the keywords that are identified by the
ID function (not the ones directly identified by get_new_token)

Lista di parole chiave per la funzione ID 
(quelli identificati direttamente dalla funzione get_new_token
 non devono essere inclusi)
"""


def _build_reserved_keywords():

    # enumerations support iteration, in definition order
    token_type_list = list(TokenType)
    start_index = token_type_list.index(TokenType.PROGRAM)
    end_index = token_type_list.index(TokenType.END)
    reserved_keywords = {
        token_type.value: token_type
        for token_type in token_type_list[start_index:end_index + 1]
    }
    return reserved_keywords

RESERVED_KEYWORDS = _build_reserved_keywords()
