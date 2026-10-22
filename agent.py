import ollama
from tools import ARACLAR
import os
import re
from dotenv import load_dotenv
from ses import dinle, konus, uyandirma_kelimesi_bekle


load_dotenv()
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:14b")


def arac_calistir(arac_cagrisi):  # Modelin istediği aracı bulup çalıştırır
    isim = arac_cagrisi.function.name  # Model hangi aracı istedi?
    argumanlar = arac_cagrisi.function.arguments  # Hangi bilgilerle istedi?

    if isim not in ARACLAR:  # Böyle bir aracımız yoksa hata mesajı döndür
        return f"Hata: '{isim}' adında bir araç yok."

    return ARACLAR[isim](**argumanlar)  # Aracı bul ve bilgilerle çalıştır

def cevap_uret(messages):  # Model nihai cevabı verene kadar araç çağırıp sonuçları geri verir
    while True:  # Model araç istemeyi bırakana kadar döner
        cevap = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=list(ARACLAR.values()),  # Sözlükteki bütün araçları modele ver
            think=False,
        )
        messages.append(cevap.message)  # Modelin mesajını geçmişe ekle

        if not cevap.message.tool_calls:  # Araç istemediyse cevap hazır demektir
            icerik = cevap.message.content
            if "</think>" in icerik:  # Model düşünme bloğunu kapanış etiketiyle sızdırdıysa
                icerik = icerik.split("</think>", 1)[1]  # Kapanış etiketinden sonrasını al, öncesini (muhakemeyi) at
            return icerik.strip()

        for arac_cagrisi in cevap.message.tool_calls:  # Araç istediyse hepsini çalıştır
            sonuc = arac_calistir(arac_cagrisi)
            print("[Araç]", arac_cagrisi.function.name, "->", sonuc)
            messages.append(
                {
                    "role": "tool",
                    "tool_name": arac_cagrisi.function.name,
                    "content": str(sonuc),
                }
            )

messages = [
    {
        "role": "system",
        "content": (
            "Sen kullanıcının kişisel asistanısın. Tarih veya saatle ilgili her işlemde, "
            "özellikle kullanıcı 'yarın', 'bugün', 'bu akşam', 'gelecek hafta' gibi göreceli "
            "bir ifade kullandığında, ASLA tarihi tahmin etme. Önce mutlaka saat_getir aracını "
            "çağırıp güncel tarih ve saati öğren, sonra hesaplamanı ona göre yap."
        ),
    }
]

while True:
    print("'Hey Jarvis' diyerek beni uyandırabilirsin...")
    uyandirma_kelimesi_bekle()
    print("Seni dinliyorum!")

    kullanici = dinle()
    print("Sen:", kullanici)

    if kullanici.strip().lower() == "çık":
        break

    messages.append({"role": "user", "content": kullanici})

    cevap = cevap_uret(messages)
    print("Asistan:", cevap)
    konus(cevap)