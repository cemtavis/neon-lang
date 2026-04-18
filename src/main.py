from lexer import Lexer
from parser import Parser, VarDecl, Assign, Print, If, While, BinOp, Num, Str, Var

class Interpreter:
    def __init__(self):
        self.env = {}

    def eval(self, node):
        if isinstance(node, Num):
            return node.value
        if isinstance(node, Str):
            return node.value
        if isinstance(node, Var):
            if node.name not in self.env:
                raise NameError(f"Hata: '{node.name}' degiskeni tanimlanmamis")
            return self.env[node.name]
        if isinstance(node, BinOp):
            left  = self.eval(node.left)
            right = self.eval(node.right)
            if node.op in ("-", "*", "/"):
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise TypeError(f"Tip Hatasi: '{node.op}' operatoru sadece sayilarla kullanilabilir")
            if node.op == "+":
                if type(left) != type(right):
                    raise TypeError(f"Tip Hatasi: Farkli tipler toplanamaz ({type(left).__name__} + {type(right).__name__})")
                return left + right
            elif node.op == "-":
                return left - right
            elif node.op == "*":
                return left * right
            elif node.op == "/":
                if right == 0:
                    raise ZeroDivisionError("Hata: Sifira bolme!")
                return left // right
        return node

    def eval_condition(self, condition):
        left_node, op, right_node = condition
        left  = self.eval(left_node)
        right = self.eval(right_node)
        if op == ">":   return left > right
        if op == "<":   return left < right
        if op == ">=":  return left >= right
        if op == "<=":  return left <= right
        if op == "==":  return left == right
        if op == "!=":  return left != right
        return False

    def run(self, ast):
        for node in ast:
            if isinstance(node, VarDecl):
                self.env[node.name] = self.eval(node.value)
            elif isinstance(node, Assign):
                if node.name not in self.env:
                    raise NameError(f"Hata: '{node.name}' degiskeni once 'let' ile tanimlanmali")
                self.env[node.name] = self.eval(node.value)
            elif isinstance(node, Print):
                print(self.eval(node.value))
            elif isinstance(node, If):
                if self.eval_condition(node.condition):
                    self.run(node.then_block)
                else:
                    self.run(node.else_block)
            elif isinstance(node, While):
                guvenlik = 0
                while self.eval_condition(node.condition):
                    self.run(node.body)
                    guvenlik += 1
                    if guvenlik > 10_000:
                        raise RuntimeError("Hata: Sonsuz dongu tespit edildi")

import os
base_dir = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.join(base_dir, "..", "examples", "example1.txt")#diğer örnekleri denemek için "example2.txt", "example3.txt" gibi değiştirebilirsiniz

with open(test_path, "r", encoding="utf-8") as f:
    code = f.read()

print("=" * 40)
print("KOD:")
print(code)
print("=" * 40)

try:
    lexer  = Lexer(code)
    tokens = lexer.tokenize()
    print("TOKENLAR:", tokens)
    print("=" * 40)
    parser = Parser(tokens)
    ast    = parser.parse()
    print("AST:", ast)
    print("=" * 40)
    print("CIKTI:")
    Interpreter().run(ast)
except (SyntaxError, NameError, TypeError, ZeroDivisionError, RuntimeError) as e:
    print(f"\n{e}")
