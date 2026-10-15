import ollama # Ollama ile konuşmamızı sağlayan kütüphaneyi içeri alıyoruz

cevap = ollama.chat(  # Modele mesaj gönderiyoruz, gelen cevap "cevap" değişkenine kaydoluyor
    model="qwen3:14b", # Hangi modelle konuşacağımız.
    messages=[{"role": "user", "content": "Merhaba, kendini tanıt."}],# Modele gönderdiğimiz konuşma.
)
print(cevap.message.content) # Modelin cevabını ekrana yazdırıyoruz