Hesap Makinesi
Python ve Tkinter kullanılarak geliştirilmiş, grafiksel kullanıcı arayüzüne sahip bilimsel hesap makinesi uygulaması.
Temel matematiksel işlemlerin yanı sıra bilimsel hesaplamalar, işlem geçmişi ve hafıza yönetimi gibi özellikler sunar.

Özellikler
Temel Matematiksel İşlemler
- Toplama, çıkarma, çarpma ve bölme
- Üs alma ve mod alma
- Parantezli matematiksel ifadeler
- Negatif sayılarla işlem yapabilme
- Yüzde hesaplamaları
- Otomatik çarpma desteği

Bilimsel Hesaplamalar
- Sinüs (sin), kosinüs (cos), tanjant (tan) ve kotanjant (cot)
- Ters trigonometrik fonksiyonlar (asin, acos, atan)
- Derece (DEG) ve radyan (RAD) açı modları
- Karekök ve küpkök
- İstenilen dereceden kök hesaplama
- Faktöriyel
- Mutlak değer
- 10 tabanında logaritma (log)
- Doğal logaritma (ln)
- Pi (π) ve Euler (e) sabitleri

Hafıza ve İşlem Geçmişi
- Son hesaplanan sonucu kullanma (Ans)
- Hafızaya ekleme (M+)
- Hafızadan çıkarma (M−)
- Hafızadaki değeri görüntüleme (MR)
- Hafızayı temizleme (MC)
- İşlem geçmişini görüntüleme
- Geçmişteki işlemleri yeniden kullanma
- İşlem geçmişini temizleme

Kullanıcı Arayüzü
- Koyu temalı grafiksel arayüz
- Bilimsel hesaplama panelini açıp kapatma
- Dinamik ekran yazı boyutu
- Fareyle etkileşimli butonlar
- Klavye desteği
- Hatalı işlemler için uyarı ve hata kontrolü

Kullanılan Teknolojiler
- Python 3.13
- Tkinter
- Math
- AST (Abstract Syntax Tree)
- Operator
- Regular Expressions (re)

Uygulama Python standart kütüphanelerini kullanır. Harici bir Python paketi gerektirmez.

Kurulum ve Çalıştırma
Gereksinimler
- Python 3.13 veya uyumlu bir sürüm
- Tkinter desteği

Adımlar
1. Depoyu bilgisayarınıza indirin veya klonlayın.
2. Proje klasörünü terminal üzerinden açın.
3. Aşağıdaki komutu çalıştırın:
python hesap_makinesi.py

Örnek Hesaplamalar
| İşlem | Sonuç |
|---|---:|
| 125+275 | 400 |
| 2^10 | 1024 |
| 5! | 120 |
| sqrt(144) | 12 |
| cbrt(27) | 3 |
| log(1000) | 3 |
| ln(e) | 1 |
| sin(30) (DEG) | 0.5 |

Güvenlik ve Hata Kontrolü
Matematiksel ifadeler Python'un `eval()` fonksiyonu kullanılmadan, AST yapısı üzerinden kontrollü biçimde değerlendirilir.
Sıfıra bölme, geçersiz matematiksel ifadeler, desteklenmeyen karmaşık sayılar ve belirli sınırları aşan hesaplamalar için hata kontrolleri uygulanır.

Geliştirici
Yunus Çakır

Bu proje, Python programlama diliyle masaüstü uygulama geliştirme ve matematiksel işlem mantığını uygulamalı olarak öğrenmek amacıyla geliştirilmiştir.
