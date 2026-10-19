from datetime import datetime

def saat_getir() -> str:
    """Şu anki tarih ve saati döndürür. Kullanıcı saat veya tarih sorarsa bu aracı kullan."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")