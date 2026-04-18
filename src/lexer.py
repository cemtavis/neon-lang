class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"{self.type}:{self.value}"

KEYWORDS = {"let", "print", "if", "else", "while"}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char and self.current_char != "\n":
            self.advance()

    def number(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token("NUMBER", int(result))

    def identifier(self):
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        if result in KEYWORDS:
            return Token("KEYWORD", result)
        return Token("IDENTIFIER", result)

    def string(self):
        self.advance()
        result = ""
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return Token("STRING", result)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "/" and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == "/":
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()

            if self.current_char == '"':
                return self.string()

            if self.current_char in "+-*":
                tok = Token("OPERATOR", self.current_char)
                self.advance()
                return tok

            if self.current_char == "/":
                tok = Token("OPERATOR", "/")
                self.advance()
                return tok

            if self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("COMPARATOR", "==")
                return Token("EQUAL", "=")

            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("COMPARATOR", "!=")
                raise Exception("Beklenmeyen karakter: !")

            if self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("COMPARATOR", ">=")
                return Token("COMPARATOR", ">")

            if self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("COMPARATOR", "<=")
                return Token("COMPARATOR", "<")

            if self.current_char == ";":
                self.advance()
                return Token("SEMICOLON", ";")

            if self.current_char == "(":
                self.advance()
                return Token("LPAREN", "(")

            if self.current_char == ")":
                self.advance()
                return Token("RPAREN", ")")

            if self.current_char == "{":
                self.advance()
                return Token("LBRACE", "{")

            if self.current_char == "}":
                self.advance()
                return Token("RBRACE", "}")

            raise Exception(f"Gecersiz karakter: '{self.current_char}'")

        return Token("EOF", None)

    def tokenize(self):
        tokens = []
        while True:
            tok = self.get_next_token()
            tokens.append(tok)
            if tok.type == "EOF":
                break
        return tokens
