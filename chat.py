import ollama  # Ollama ile konuşmamızı sağlayan kütüphane

messages = []  # Konuşma geçmişi burada tutulur, başta boş

while True:  # "q" yazana kadar sürekli döner
    kullanici = input("Sen: ")  # Klavyeden mesaj al

    if kullanici == "q":  # "q" yazılırsa döngüden çık
        break

    messages.append({"role": "user", "content": kullanici})  # Mesajımızı geçmişe ekle

    cevap = ollama.chat(model="qwen3:14b", messages=messages)  # Bütün geçmişi modele gönder

    model_cevabi = cevap.message.content  # Modelin yazdığı metni al
    print("Asistan:", model_cevabi)  # Ekrana yazdır

    messages.append({"role": "assistant", "content": model_cevabi})  # Cevabı da geçmişe ekle