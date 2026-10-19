import json
import os
from datetime import datetime

DOSYA = "notlar.json"  # Notların saklandığı dosyanın adı

def _notlari_oku():  # Dosyadaki notları Python listesine çevirip döndürür (iç kullanım, başına _ konuldu)
    if not os.path.exists(DOSYA): # Dosya hiç yoksa (ilk çalıştırma)
        return [] # Boş liste döndür, hata verme
    with open(DOSYA, "r", encoding="utf-8") as f:  # Dosyayı Türkçe karakterler bozulmadan aç
        return json.load(f)  # İçeriği Python listesine çevirip döndür

def not_ekle(icerik: str) -> str: # Modelin çağıracağı araç: yeni bir not kaydeder
    """Kullanıcının söylediği bir notu kaydeder. Kullanıcı 'şunu not al', 'hatırlat' gibi bir şey söylediğinde bu aracı kullan.""" # Model bu açıklamayı okuyup ne zaman çağıracağına karar verir
    notlar = _notlari_oku() # Önce mevcut notları yükle
    notlar.append({   # Yeni notu listeye ekle
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),  # Not ne zaman alındı
        "icerik": icerik,  # Notun kendisi
    })
    with open(DOSYA, "w", encoding="utf-8") as f:  # Dosyayı yazma modunda aç
        json.dump(notlar, f, ensure_ascii=False, indent=2)   # Güncellenmiş listeyi dosyaya geri yaz (ensure_ascii=False -> Türkçe karakterler bozulmasın)
    return "Not kaydedildi."  # Modele dönecek sonuç mesajı

def notlari_listele() -> str:
    """Kayıtlı tüm notları listeler. Kullanıcı notlarını sorduğunda bu aracı kullan.""" # Model bu açıklamayı okuyup ne zaman çağıracağına karar verir
    notlar = _notlari_oku() # Dosyadaki notları yükle
    if not notlar: # Hiç not yoksa
        return "Henüz hiç not yok."  # Kullanıcıya bunu bildir
    return "\n".join(f"- [{n['tarih']}] {n['icerik']}" for n in notlar)  # Her notu "- [tarih] içerik" formatında alt alta yaz