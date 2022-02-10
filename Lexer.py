from Token import TokenType, Token, RESERVED_KEYWORDS
from Errors import LexerError


class Lexer(object):
    def __init__(self, text):

        self.text = text
        self.pos = 0    # Position in the text/ Posizione nel testo
        self.current_char = self.text[self.pos]
        self.lineno = 1
        self.column = 1

    def error(self):

        s = "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
            lexeme=self.current_char,
            lineno=self.lineno,
            column=self.column,
        )
        raise LexerError(message=s)

    def advance(self, steps=1):
        # Method to advance in the text, setting current_char to the new character
        # Metodo per avanzare di un carattere nel testo, current_char viene assegnato al nuovo carattere

        if self.current_char == '\n':
            self.lineno += 1
            self.column = 0
        self.pos += steps
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Reached the EOF
        else:
            self.current_char = self.text[self.pos]
            self.column += steps

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        # Method called if the char { is found, skips until a } is found
        # Metodo per saltare i commenti (tipo: { .... })

        while self.current_char != '}':
            self.advance()
        self.advance()  # the closing curly brace

    def string(self) -> Token:

        token = Token(type=None, value=None, lineno=self.lineno, column=self.column)

        result = ''

        while self.current_char != '"' and self.current_char != '\'':
            result += self.current_char
            self.advance()
        self.advance()

        token.type = TokenType.STRING
        token.value = str(result)

        return token

    def number(self) -> Token:

        # Returns an integer or a float
        # Ritorna un numero intero o decimale

        token = Token(type=None, value=None, lineno=self.lineno, column=self.column)

        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token.type = TokenType.REAL_CONST
            token.value = float(result)
        else:
            token.type = TokenType.INTEGER_CONST
            token.value = int(result)

        return token

    def _id(self) -> Token:
        # Finds reserved keywords and identifiers
        token = Token(type=None, value=None, lineno=self.lineno, column=self.column)

        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token_type = RESERVED_KEYWORDS.get(result.upper())

        if token_type is None:
            token.type = TokenType.ID
            token.value = result

        elif token_type == TokenType.ARRAY:
            print("Found array")    # Returns token with type ARRAY and value [range min, range max]
            token.type = token_type
            token.value = result.upper()

        else:   # Found a reserved keyword
            token.type = token_type
            token.value = result.upper()

        return token

    def get_index(self):
        index = self.number_int()
        if self.current_char == "]":
            self.advance()
        else:
            print("Did not find ] at end of range")
            self.error()
        return index

    def check_if_index(self):
        peek_pos = self.pos + 1
        while peek_pos < len(self.text) + 1 and self.text[peek_pos] != ']':
            peek_pos += 1
            if self.text[peek_pos] == '[':
                return False
            if self.text[peek_pos] == '.':
                return False
        return True

    def get_range(self):
        lower_range = self.number_int()
        while self.current_char == ".":
            self.advance()
        upper_range = self.number_int()
        if self.current_char == "]":
            self.advance()
        else:
            print("Did not find ] at end of range")
            self.error()

        return lower_range, upper_range

    def number_int(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        result = int(result)
        return result

    def get_next_token(self):

        # Main function to identify tokens / Funzione principale per identificare i token

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char == '[':
                if self.check_if_index():
                    print("FOUND INDEX")






            if self.current_char == '[':  # Modify
                self.advance()
                if self.check_if_index():
                    index = self.get_index()
                    token = Token(
                        type=TokenType.INDEX,
                        value=index,  # Value is an int
                        lineno=self.lineno,
                        column=self.column,
                    )
                    return token
                else:
                    range_ = self.get_range()
                    token = Token(
                        type=TokenType.RANGE,
                        value=range_,  # The value is a tuple (low_range, high_index)
                        lineno=self.lineno,
                        column=self.column,
                    )
                    return token

            if self.current_char == '"' or self.current_char == '\'':  # For the print function
                self.advance()
                return self.string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            # for two character tokens
            try:
                token_type = TokenType(self.current_char + self.peek())
            except ValueError:
                pass
            else:
                token = Token(
                    type=token_type,
                    value=token_type.value,  # e.g. ':=', '<=', etc
                    lineno=self.lineno,
                    column=self.column,
                )
                self.advance(steps=2)
                return token

            # for single character tokens
            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                # no enum member with value equal to self.current_char
                self.error()
            else:
                # create a token with a single-character lexeme as its value
                token = Token(
                    type=token_type,
                    value=token_type.value,  # e.g. ';', '.', etc
                    lineno=self.lineno,
                    column=self.column,
                )
                self.advance()
                return token

        return Token(type=TokenType.EOF, value=None)
