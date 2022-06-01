from Token import TokenType, Token, RESERVED_KEYWORDS
from src.Errors import LexerError


class Lexer(object):

    def __init__(self, text: str):
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

    def advance(self, steps: int = 1) -> None:
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

    def peek(self) -> None | str:
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self) -> None:
        # Method called if the char { is found, skips until a } is found
        # Metodo per saltare i commenti (tipo: { .... })

        while self.current_char != '}':
            self.advance()
        self.advance()  # the closing curly brace

    def skip_single_line_comment(self) -> None:
        while self.current_char != '\n':
            self.advance()
        self.advance()

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

        token = Token(type=None, value=None, lineno=self.lineno, column=self.column)
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.' and self.peek().isdigit():
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
            token.type = token_type
            token.value = result.upper()

        else:   # Found a reserved keyword
            token.type = token_type
            token.value = result.upper()

        return token

    def get_next_token(self) -> Token:

        # Main function to identify tokens / Funzione principale per identificare i token

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.skip_single_line_comment()
                continue

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
