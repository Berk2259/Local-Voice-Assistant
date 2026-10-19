import ollama
from tools import ARACLAR
import os
import re
from dotenv import load_dotenv

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

messages = []  # Konuşma geçmişi, başta boş

while True:  # "q" yazana kadar sürekli döner
    kullanici = input("Sen: ")  # Klavyeden mesaj al

    if kullanici == "q":  # "q" yazılırsa çık
        break

    messages.append({"role": "user", "content": kullanici})  # Mesajımızı geçmişe ekle

    cevap = cevap_uret(messages)  # Model gerekirse araç çağırır, sonunda cevabı verir
    print("Asistan:", cevap)