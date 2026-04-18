# Yapay Zeka Kullanım Belgesi (ai_prompts.md)

Bu dosya, Neon dili projesinde Claude (Anthropic) yapay zeka aracından alınan destekleri belgelemektedir.

---

## Kullanılan Araç

- **Araç:** Claude (Anthropic) — claude.ai
- **Tarih Aralığı:** Nisan 2026

---

## 1. Dil Tasarımı Aşaması

**Tarih:** Nisan 2026

**Benim yaptıklarım:**
- Dilin hangi özelliklere sahip olacağına karar verdim: değişken tanımlama, if/else, while döngüsü, print komutu
- `int` ve `string` veri tiplerini desteklemesine karar verdim
- Sözdiziminin `let x = 10;` şeklinde noktalı virgülle bitmesini istedim
- Dilin adına karar verdim: **Neon**

**Yapay zekadan ne istedim:**
> "dil seçimi beraber yapalım" — isim seçimi için fikir aldım, son kararı kendim verdim.

**Yapay zekanın katkısı:** Sadece isim önerisi sundu, dil tasarım kararlarını ben verdim.

---

## 2. Lexer Geliştirme

**Tarih:** Nisan 2026

**Benim yaptıklarım:**
- Lexer'ın genel yapısını kurdum: `Token` sınıfı, `advance()`, `skip_whitespace()`, `number()`, `identifier()`, `string()` metodları
- `KEYWORD`, `IDENTIFIER`, `NUMBER`, `STRING`, `OPERATOR`, `SEMICOLON` gibi token tiplerini tasarladım
- `get_next_token()` ve `tokenize()` metodlarını yazdım

**Karşılaştığım sorun:**
`//` yorum satırlarını tanımıyordu. `/` karakterini iki ayrı `OPERATOR` token'ı olarak üretiyordu.

**Yapay zekaya sorduğum soru:**
> "if elsei eklemeye çalışıyorum fakat çıktıda büyük veya küçük yazmıyor"

**Yapay zekanın katkısı:**
`//` için özel kontrol eklenmesi gerektiğini açıkladı. Ayrıca `==`, `!=`, `>=`, `<=` operatörleri için de iki karakterli token üretimi nasıl yapılır gösterdi.

**Benim entegrasyonum:**
Açıklamayı anlayarak kendi lexer kodum üzerine uyguladım.

---

## 3. Parser Geliştirme

**Tarih:** Nisan 2026

**Benim yaptıklarım:**
- `VarDecl`, `Print`, `If` AST sınıflarını tasarladım
- `parse()`, `let()`, `print_stmt()`, `if_stmt()` metodlarını yazdım
- `expression()`, `term()`, `factor()` metodları ile matematiksel önceliği uyguladım

**Karşılaştığım sorun:**
`if_stmt` içinde condition'daki değerler AST node'u olarak değil ham string/int olarak saklanıyordu. Bu yüzden interpreter değişkeni sembol tablosunda bulamıyordu.

**Yapay zekaya sorduğum soru:**
> "AST'de VarDecl(x, 10) yazıyor, büyük veya küçük yazmıyor"

**Yapay zekanın katkısı:**
`Num`, `Str`, `Var`, `BinOp` sınıflarının neden gerekli olduğunu açıkladı. `factor()` metodunun ham değer yerine bu sınıfların örneklerini döndürmesi gerektiğini gösterdi. `while` döngüsü için `While` sınıfı ve `while_stmt()` metodu nasıl yazılır anlattı.

**Benim entegrasyonum:**
Kendi parser kodum üzerinde hangi metodların değişmesi gerektiğini anlayarak uyguladım. `assign_stmt()` metodunu ekledim.

---

## 4. Interpreter Geliştirme

**Tarih:** Nisan 2026

**Benim yaptıklarım:**
- `Interpreter` sınıfını ve `env` sembol tablosunu tasarladım
- `eval()` ve `run()` metodlarının genel yapısını kurdum
- `VarDecl`, `Print`, `If` düğümlerinin nasıl çalıştırılacağını kodladım

**Karşılaştığım sorun:**
`eval()` metodu `Num`, `Str`, `Var` gibi AST sınıflarını tanımıyordu çünkü parser henüz bunları üretmiyordu.

**Yapay zekaya sorduğum soru:**
> "OUTPUT kısmında hiçbir şey çıkmıyor"

**Yapay zekanın katkısı:**
`isinstance(node, Num)` kontrolleri ile her AST sınıfı için ayrı `eval()` dalı yazılması gerektiğini açıkladı. Tip kontrolü (string + int hatası), sıfıra bölme ve sonsuz döngü korumasının nasıl ekleneceğini gösterdi.

**Benim entegrasyonum:**
`eval_condition()` metodunu kendim yazdım. Hata mesajlarını Türkçe olarak düzenledim.

---

## 5. Test ve Hata Ayıklama

**Tarih:** Nisan 2026

**Benim yaptıklarım:**
- `test.txt` dosyasını yazarak kodu test ettim
- Terminal çıktılarını okuyarak hangi aşamada hata olduğunu tespit ettim
- Tokenlar ve AST çıktısına bakarak sorunun nerede olduğunu analiz ettim

**Yapay zekaya sorduğum soru:**
> "TOKENLAR satırında while IDENTIFIER olarak görünüyor, KEYWORD olması lazım"

**Yapay zekanın katkısı:**
`KEYWORDS` setine `"while"` eklenmesi gerektiğini belirtti.

---

## Özet Tablosu

| Aşama | Benim Katkım | Yapay Zeka Katkısı |
|---|---|---|
| Dil Tasarımı | Tüm kararlar bana ait | İsim önerisi |
| Lexer | Genel yapı ve tüm metodlar | `//` ve çok karakterli operatör düzeltmesi |
| Parser | AST sınıfları, tüm parse metodları | `Num/Str/Var/BinOp` sınıfı mantığı, `while` eklenmesi |
| Interpreter | `eval()` ve `run()` yapısı | Tip kontrolü ve koruma mekanizmaları |
| Test | Tüm testler | Hata mesajlarının yorumlanması |
