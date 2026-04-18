# Neon Programming Language

Neon, Python ile geliştirilmiş sade ve öğrenilebilir bir programlama dilidir.  
Lexer, Parser ve Interpreter aşamalarından oluşan tam bir yorumlayıcıya sahiptir.

---

## Özellikler

- `let` ile değişken tanımlama
- `int` ve `string` veri tipleri
- `+`, `-`, `*`, `/` aritmetik operatörler
- `>`, `<`, `>=`, `<=`, `==`, `!=` karşılaştırma operatörleri
- `if / else` koşullu ifadeler
- `while` döngüsü
- `print()` ile ekrana çıktı
- `//` ile yorum satırı
- Tip kontrolü (string ile sayı toplamaya çalışınca hata verir)
- Anlamlı hata mesajları (SyntaxError, NameError, TypeError)

---

## Dosya Yapısı

```
dilim/
├── src/
│   ├── lexer.py       # Kaynak kodu token'lara ayırır
│   ├── parser.py      # Token'lardan AST üretir
│   └── main.py        # AST'yi çalıştıran interpreter
├── examples/
│   ├── example1.txt   # if/else örneği
│   ├── example2.txt   # while döngüsü örneği
│   └── example3.txt   # matematik ve string örneği
├── ai_prompts.md      # Yapay zeka kullanım belgesi
└── README.md
```

---

## Nasıl Çalıştırılır

### Gereksinimler
- Python 3.8 veya üzeri

### Kurulum
```bash
git clone https://github.com/kullanici_adi/neon-lang.git
cd neon-lang
```

### Çalıştırma
```bash
cd src
python main.py
```

`main.py` varsayılan olarak `examples/` klasöründeki `test.txt` dosyasını çalıştırır.  
Farklı bir dosya test etmek için `main.py` içindeki `test_path` satırını değiştirebilirsiniz.

---

## Sözdizimi (Syntax) Örnekleri

```neon
// Değişken tanımlama
let x = 10;
let mesaj = "Merhaba";

// if / else
if (x > 5) {
    print("buyuk");
} else {
    print("kucuk");
}

// while döngüsü
let sayac = 0;
while (sayac < 3) {
    print(sayac);
    sayac = sayac + 1;
}

// print
print(mesaj);
```

---

## Gramer (BNF / CFG)

```
program        ::= statement*

statement      ::= var_decl
                 | assign_stmt
                 | print_stmt
                 | if_stmt
                 | while_stmt

var_decl       ::= "let" IDENTIFIER "=" expression ";"

assign_stmt    ::= IDENTIFIER "=" expression ";"

print_stmt     ::= "print" "(" expression ")" ";"

if_stmt        ::= "if" "(" condition ")" "{" statement* "}"
                   ( "else" "{" statement* "}" )?

while_stmt     ::= "while" "(" condition ")" "{" statement* "}"

condition      ::= expression COMPARATOR expression

expression     ::= term ( ("+" | "-") term )*

term           ::= factor ( ("*" | "/") factor )*

factor         ::= NUMBER
                 | STRING
                 | IDENTIFIER
                 | "(" expression ")"

COMPARATOR     ::= ">" | "<" | ">=" | "<=" | "==" | "!="

NUMBER         ::= [0-9]+

STRING         ::= '"' [herhangi bir karakter]* '"'

IDENTIFIER     ::= [a-zA-Z_][a-zA-Z0-9_]*
```

---

## Mimariye Genel Bakış

### 1. Lexer (`lexer.py`)
Kaynak kodu karakter karakter okur ve anlamlı token'lara dönüştürür.  
Örnek: `let x = 10;` → `[KEYWORD:let, IDENTIFIER:x, EQUAL:=, NUMBER:10, SEMICOLON:;]`

### 2. Parser (`parser.py`)
Token dizisini alır, gramer kurallarına göre kontrol eder ve bir **Soyut Sözdizim Ağacı (AST)** üretir.  
Hatalı sözdizimde anlamlı `SyntaxError` fırlatır.

### 3. Interpreter (`main.py`)
AST'yi yukarıdan aşağıya dolaşarak çalıştırır.  
Değişkenleri bir sembol tablosunda (`env` dict) tutar.  
Tip uyumsuzluklarını tespit ederek `TypeError` fırlatır.

---

## Geliştirici

**Hüseyin Cem Taviş**  
Programlama Dilleri Dersi — 2025/2026
