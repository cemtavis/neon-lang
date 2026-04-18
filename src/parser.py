# AST Dugum Siniflari


class VarDecl:
    """let x = ifade;"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VarDecl({self.name}, {self.value})"


class Assign:
    """x = ifade;"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assign({self.name}, {self.value})"


class Print:
    """print(ifade);"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Print({self.value})"


class If:
    """if (kosul) { ... } else { ... }"""
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"If({self.condition}, {self.then_block}, {self.else_block})"


class While:
    """while (kosul) { ... }"""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class BinOp:
    """sol op sag  (ornegin: x + 5)"""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"


class Num:
    """Sayisal sabit"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"


class Str:
    """String sabit"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Str({self.value})"


class Var:
    """Degisken referansi"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"



# Parser


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0]

    # ----- yardimci -----

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def expect(self, type_):
        """Beklenen token tipini kontrol et, ilerle."""
        if self.current.type != type_:
            raise SyntaxError(
                f"Syntax Error: '{type_}' beklendi ama '{self.current.type}:{self.current.value}' bulundu"
            )
        self.advance()

    # ------- ana dongu ------

    def parse(self):
        statements = []
        while self.current.type != "EOF":
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def statement(self):
        tok = self.current

        if tok.type == "KEYWORD" and tok.value == "let":
            return self.let_stmt()

        if tok.type == "KEYWORD" and tok.value == "print":
            return self.print_stmt()

        if tok.type == "KEYWORD" and tok.value == "if":
            return self.if_stmt()

        if tok.type == "KEYWORD" and tok.value == "while":
            return self.while_stmt()

        # x = ifade;  atama
        if tok.type == "IDENTIFIER":
            next_tok = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_tok and next_tok.type == "EQUAL":
                return self.assign_stmt()

        # taninamayan token: atla
        self.advance()
        return None

    # ------ let ------

    def let_stmt(self):
        self.advance()  # let

        if self.current.type != "IDENTIFIER":
            raise SyntaxError(f"Syntax Error: 'let' sonrasi degisken adi beklendi")
        name = self.current.value
        self.advance()

        self.expect("EQUAL")          # =
        value = self.expression()
        self.expect("SEMICOLON")      # ;

        return VarDecl(name, value)

    # ----- atama -----

    def assign_stmt(self):
        name = self.current.value
        self.advance()          # degisken adi
        self.expect("EQUAL")    # =
        value = self.expression()
        self.expect("SEMICOLON")  # ;
        return Assign(name, value)

    # ------ print -----

    def print_stmt(self):
        self.advance()            # print
        self.expect("LPAREN")     # (
        value = self.expression()
        self.expect("RPAREN")     # )
        self.expect("SEMICOLON")  # ;
        return Print(value)

    # ------ if -------

    def if_stmt(self):
        self.advance()         # if
        self.expect("LPAREN")  # (
        condition = self.condition()
        self.expect("RPAREN")  # )
        self.expect("LBRACE")  # {

        then_block = self.block()

        self.expect("RBRACE")  # }

        else_block = []
        if self.current.type == "KEYWORD" and self.current.value == "else":
            self.advance()         # else
            self.expect("LBRACE")  # {
            else_block = self.block()
            self.expect("RBRACE")  # }

        return If(condition, then_block, else_block)

    # ------ while ------

    def while_stmt(self):
        self.advance()         # while
        self.expect("LPAREN")  # (
        condition = self.condition()
        self.expect("RPAREN")  # )
        self.expect("LBRACE")  # {

        body = self.block()

        self.expect("RBRACE")  # }

        return While(condition, body)

    # ------- blok (RBRACE'e kadar ifadeler) ------

    def block(self):
        stmts = []
        while self.current.type != "RBRACE" and self.current.type != "EOF":
            stmt = self.statement()
            if stmt is not None:
                stmts.append(stmt)
        return stmts

    # ------ kosul -------

    def condition(self):
        left = self.expression()

        if self.current.type != "COMPARATOR":
            raise SyntaxError(
                f"Syntax Error: Karsilastirma operatoru beklendi, bulundu: {self.current}"
            )
        op = self.current.value
        self.advance()

        right = self.expression()
        return (left, op, right)

    # ------ ifade (+ -) -------

    def expression(self):
        result = self.term()

        while self.current.type == "OPERATOR" and self.current.value in ("+", "-"):
            op = self.current.value
            self.advance()
            right = self.term()
            result = BinOp(result, op, right)

        return result

    # ------- terim (* /) --------

    def term(self):
        result = self.factor()

        while self.current.type == "OPERATOR" and self.current.value in ("*", "/"):
            op = self.current.value
            self.advance()
            right = self.factor()
            result = BinOp(result, op, right)

        return result

    # ------- faktor -----

    def factor(self):
        tok = self.current

        if tok.type == "NUMBER":
            self.advance()
            return Num(tok.value)

        if tok.type == "STRING":
            self.advance()
            return Str(tok.value)

        if tok.type == "IDENTIFIER":
            self.advance()
            return Var(tok.name if hasattr(tok, "name") else tok.value)

        if tok.type == "LPAREN":
            self.advance()       # (
            expr = self.expression()
            self.expect("RPAREN")  # )
            return expr

        raise SyntaxError(f"Syntax Error: Beklenmeyen token: {tok}")
