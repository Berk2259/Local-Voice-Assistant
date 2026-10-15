<h1 align="center">Local Voice Assistant</h1>

<p align="center">
  Türkçe konuşan, verilerin kendi bilgisayarımda kaldığı kişisel yapay zekâ asistanı.

## Amaç

Mail, takvim ve notlarınla ilgilenen, sesle konuşabildiğin bir asistan yapmak. Yapay zekâ modeli tamamen yerelde çalışır, verilerin buluta gönderilmez.

## Durum

- [x] Yerel modelle (Qwen3 14B) Python'dan konuşma
- [x] Modelin araç çağırması (tool calling)

## Ekran Görüntüleri

### İlk konuşma

<img src="images/images1.png" alt="Qwen3 ile ilk konuşma" width="700">

### Sohbet ve hafıza

<img src="images/images2.png" alt="Hafıza testi" width="700">

### Araç kullanımı (tool calling)

Model saati bilmiyor. `saat_getir` aracını çağırmak istiyor, sonucu alıp cevap yazıyor.

<img src="images/images3.png" alt="Tool calling testi" width="300">

## Teknolojiler

- Python
- Ollama
- Qwen3 14B