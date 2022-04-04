# Token types / tipologie di Token

from enum import Enum


class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):

        # Printing function for objects of Token type
        # Funzione di stampa per i Token

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
    SEMI = ';'
    DOT = '.'
    COLON = ':'
    QUOTE = '"'
    S_QUOTE = '\''
    COMMA = ','
    # Reserved keywords
    PROGRAM = 'PROGRAM'
    # Special two character tokens
    GREAT_EQ = '>='
    LESS_EQ = '<='
    NOT_EQ = '<>'
    ASSIGN = ':='
    # Other reserved keywords
    ARRAY = 'ARRAY'
    OF = 'OF'
    RANGE = 'RANGE'
    INDEX = 'INDEX'
    INTEGER = 'INTEGER'  # Tokens of the types INT and REAL
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
    FUNCTION = 'FUNCTION'
    WRITELN = 'WRITELN'
    READLN = 'READLN'
    WHILE = 'WHILE'
    REPEAT = 'REPEAT'
    UNTIL = 'UNTIL'
    SETLENGTH = 'SETLENGTH'
    DO = 'DO'
    END = 'END'
    EOF = 'EOF'
    # Other keywords
    INTEGER_CONST = 'INTEGER_CONST'  # Tokens of variables of type INT and REAL
    REAL_CONST = 'REAL_CONST'
    ID = 'ID'


"""
List of reserved keywords
Lista di parole chiave
"""


def _build_reserved_keywords():

    # enumerations support iteration, in definition order
    token_type_list = list(TokenType)
    start_index = token_type_list.index(TokenType.PROGRAM)
    end_index = token_type_list.index(TokenType.END)
    keyword_dict = {
        token_type.value: token_type
        for token_type in token_type_list[start_index:end_index + 1]
    }
    return keyword_dict


RESERVED_KEYWORDS = _build_reserved_keywords()
