import subprocess  # Uygulamaları başlatmak için

UYGULAMALAR = {  # Yaygın uygulama adları -> Windows komutu eşlemesi
    "not defteri": "notepad",  # "not defteri" denirse Windows'un "notepad" komutunu çalıştır
    "hesap makinesi": "calc", # "hesap makinesi" denirse "calc" komutunu çalıştır
    "chrome": "chrome", # "chrome" denirse "chrome" komutunu çalıştır
    "explorer": "explorer", # "explorer" denirse dosya gezginini aç 
    "paint": "mspaint", # "paint" denirse "mspaint" komutunu çalıştır
}

def uygulama_ac(isim: str) -> str:  # Modelin çağıracağı araç: istenen uygulamayı açar
    """Bilgisayarda bir uygulama açar (ör. not defteri, hesap makinesi, chrome). Kullanıcı bir uygulamayı açmanı istediğinde bu aracı kullan.""" # Model bu açıklamayı okuyup ne zaman çağıracağına karar verir
    komut = UYGULAMALAR.get(isim.lower(), isim)  # Sözlükte varsa Windows komutuna çevir, yoksa (büyük/küçük harf farkı gözetmeden) direkt söylenen ismi dene
    try:
        subprocess.Popen(komut, shell=True)   # Uygulamayı başlat, kapanmasını beklemeden hemen devam et
        return f"{isim} açılıyor."  # Başarılı olursa modele/kullanıcıya bildir
    except Exception as e: # Uygulama bulunamazsa ya da başka bir hata olursa buraya düşer
        return f"{isim} açılamadı: {e}"  # Hatanın sebebiyle birlikte kullanıcıya bildir