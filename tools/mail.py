from googleapiclient.discovery import build  # Gmail servisine bağlanmak için
from .google_auth import servis_al  # Az önce yazdığımız ortak kimlik doğrulama fonksiyonu

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]  # Sadece okuma izni istiyoruz, mail silme/gönderme yok

def son_mailleri_getir(adet: int = 5) -> str:  # Modelin çağıracağı araç: son N maili özetler
    """Gmail gelen kutusundaki en son mailleri getirir. Kullanıcı maillerini sorduğunda bu aracı kullan."""
    kimlik = servis_al(SCOPES, "token_gmail.json")  # İzin al / kaydedilmiş token'ı kullan
    servis = build("gmail", "v1", credentials=kimlik)  # Gmail API bağlantısını kur

    sonuc = servis.users().messages().list(userId="me", maxResults=adet).execute()  # Son N mailin ID listesini al
    mesajlar = sonuc.get("messages", [])  # Liste boşsa boş liste dön

    if not mesajlar:
        return "Gelen kutusunda mail yok."

    satirlar = []
    for m in mesajlar:  # Her mail ID'si için detay çek
        detay = servis.users().messages().get(
            userId="me", id=m["id"], format="metadata", metadataHeaders=["From", "Subject"]
        ).execute()  # Sadece gönderen ve konu başlıklarını iste (hızlı olsun diye tüm içeriği çekmiyoruz)

        basliklar = {h["name"]: h["value"] for h in detay["payload"]["headers"]}  # Header listesini sözlüğe çevir
        gonderen = basliklar.get("From", "Bilinmiyor")
        konu = basliklar.get("Subject", "(konu yok)")
        satirlar.append(f"- {gonderen}: {konu}")

    return "\n".join(satirlar)