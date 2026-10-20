<h1 align="center">Local Voice Assistant</h1>

<p align="center">
  Türkçe konuşan, verilerin kendi bilgisayarımda kaldığı kişisel yapay zekâ asistanı.

## Amaç

Mail, takvim ve notlarınla ilgilenen, sesle konuşabildiğin bir asistan yapmak. Yapay zekâ modeli tamamen yerelde çalışır, verilerin buluta gönderilmez.

## Durum

- [x] Yerel modelle (Qwen3 14B) Python'dan konuşma
- [x] Modelin araç çağırması (tool calling)
- [x] Araç kullanan ajan döngüsü
- [x] Araçları `tools/` paketi altında modüler yapıya taşıma
- [x] Not alma aracı (not_ekle, notlari_listele)
- [x] Uygulama açma aracı (uygulama_ac)
- [x] Google OAuth kimlik doğrulama (google_auth.py)
- [x] Gmail entegrasyonu (son_mailleri_getir)
- [x] Google Takvim entegrasyonu (etkinlik_ekle, yaklasan_etkinlikler)
- [ ] Sesli giriş (Speech-to-Text)
- [ ] Sesli çıkış (Text-to-Speech)

## Ekran Görüntüleri

### İlk konuşma

<img src="images/images1.png" alt="Qwen3 ile ilk konuşma" width="1000">

### Sohbet ve hafıza

<img src="images/images2.png" alt="Hafıza testi" width="700">

### Araç kullanımı (tool calling)

Model saati bilmiyor. `saat_getir` aracını çağırmak istiyor, sonucu alıp cevap yazıyor.

<img src="images/images3.png" alt="Tool calling testi" width="300">

### Ajan döngüsü

Model gerektiğinde araç çağırıyor, gerekmediğinde doğrudan cevap veriyor. Konuşmayı da hatırlıyor.

<img src="images/images4.png" alt="Ajan döngüsü" width="300">


### Mail entegrasyonu

Model, Gmail gelen kutusundaki son mailleri `son_mailleri_getir` aracıyla çekip özetliyor.

<img src="images/images5.png" alt="Gmail entegrasyonu testi" width="700">


### Takvim entegrasyonu

Model, `etkinlik_ekle` ile Google Takvim'e yeni bir etkinlik ekliyor, `yaklasan_etkinlikler` ile de yaklaşan etkinlikleri listeliyor.

<img src="images/images6.png" alt="Google Takvim entegrasyonu testi" width="1000">

## Teknolojiler

- Python
- Ollama
- Qwen3 14B
- Google Gmail API
- Google Calendar API