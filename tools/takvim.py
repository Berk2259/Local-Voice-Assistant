from datetime import datetime, timedelta  # Etkinlik başlangıç/bitiş saatini hesaplamak için
from googleapiclient.discovery import build  # Calendar servisine bağlanmak için
from .google_auth import servis_al  # Ortak kimlik doğrulama fonksiyonu

SCOPES = ["https://www.googleapis.com/auth/calendar"]  # Hem okuma hem etkinlik ekleme izni (mail'den farklı, bu yüzden ayrı token dosyası kullanacağız)
ZAMAN_DILIMI = "Europe/Istanbul"  # Etkinlik saatlerini doğru gösterebilmek için

def etkinlik_ekle(baslik: str, tarih: str, saat: str, sure_dakika: int = 60) -> str:  # Modelin çağıracağı araç: takvime yeni etkinlik ekler
    """Google Takvim'e yeni bir etkinlik ekler. tarih 'YYYY-MM-DD', saat 'HH:MM' formatında olmalı. Kullanıcı takvime bir şey eklemeni istediğinde bu aracı kullan."""
    kimlik = servis_al(SCOPES, "token_calendar.json")  # İzin al / kaydedilmiş token'ı kullan
    servis = build("calendar", "v3", credentials=kimlik)  # Calendar API bağlantısını kur

    baslangic = datetime.strptime(f"{tarih} {saat}", "%Y-%m-%d %H:%M")  # Verilen tarih+saati Python datetime'a çevir
    bitis = baslangic + timedelta(minutes=sure_dakika)  # Süreyi ekleyip bitiş zamanını hesapla

    etkinlik = {  # Google Calendar API'nin beklediği format
        "summary": baslik,
        "start": {"dateTime": baslangic.isoformat(), "timeZone": ZAMAN_DILIMI},
        "end": {"dateTime": bitis.isoformat(), "timeZone": ZAMAN_DILIMI},
    }

    servis.events().insert(calendarId="primary", body=etkinlik).execute()  # Etkinliği ana takvime ekle
    return f"'{baslik}' etkinliği {tarih} {saat} için eklendi."

def yaklasan_etkinlikler(adet: int = 5) -> str:  # Modelin çağıracağı araç: yaklaşan etkinlikleri listeler
    """Takvimdeki yaklaşan etkinlikleri listeler. Kullanıcı takviminde ne olduğunu sorduğunda bu aracı kullan."""
    kimlik = servis_al(SCOPES, "token_calendar.json")
    servis = build("calendar", "v3", credentials=kimlik)

    simdi = datetime.utcnow().isoformat() + "Z"  # Google API UTC zaman formatı bekliyor
    sonuc = servis.events().list(
        calendarId="primary", timeMin=simdi, maxResults=adet,
        singleEvents=True, orderBy="startTime",
    ).execute()  # Şu andan itibaren en yakın N etkinliği, zamana göre sıralı getir
    etkinlikler = sonuc.get("items", [])

    if not etkinlikler:
        return "Yaklaşan etkinlik yok."

    satirlar = []
    for e in etkinlikler:  # Her etkinliği okunabilir bir satıra çevir
        baslangic = e["start"].get("dateTime", e["start"].get("date"))  # Tüm gün etkinliklerde "date" kullanılır
        satirlar.append(f"- {baslangic}: {e.get('summary', '(başlıksız)')}")

    return "\n".join(satirlar)