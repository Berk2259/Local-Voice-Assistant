from datetime import datetime  # Tarih ve saat işlemleri için hazır Python modülü
import ollama

#Anlık Gün ve Saati getiren fonksiyon
def saat_getir() -> str:
    """Şu anki tarih ve saati döndürür. Kullanıcı saat veya tarih sorarsa bu aracı kullan.""" #Bu kısım python fonksiyonlarındaki docstring kısmı model bu fonksiyonu çağıracağı zaman bu kısmı okur
    return datetime.now().strftime("%Y-%m-%d %H:%M")

messages = [{"role": "user", "content": "Saat kaç?"}] # Modele soracağımız soru

cevap = ollama.chat(
    model="qwen3:14b",
    messages=messages,
    tools=[saat_getir],  # Modele "elinde bu araç var" diyoruz
    think=False,
)

messages.append(cevap.message)  # Modelin "aracı çağır" mesajını konuşma geçmişine ekle

for arac_cagrisi in cevap.message.tool_calls:  # Model hangi araçları çağırmak istedi?
    if arac_cagrisi.function.name == "saat_getir":  # İstenen araç saat_getir mi?
        sonuc = saat_getir()  # Fonksiyonu gerçekten biz çalıştırıyoruz
        print("Araç sonucu:", sonuc)
        messages.append({"role": "tool", "tool_name": "saat_getir", "content": sonuc})  # Sonucu modele "araç cevabı" olarak ver

son_cevap = ollama.chat(
    model="qwen3:14b",
    messages=messages, 
    tools=[saat_getir],
    think=False,  # Düşünme modunu kapat, cevap doğrudan content'e yazılsın
)  # Model sonucu görerek cevap yazsın
print("Asistan:", son_cevap.message.content)