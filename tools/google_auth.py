import os  # Dosya var mı kontrolü için
from google.auth.transport.requests import Request  # Süresi dolan token'ı yenilemek için
from google.oauth2.credentials import Credentials  # Kaydedilmiş token'ı okumak için
from google_auth_oauthlib.flow import InstalledAppFlow  # İlk izin alma akışını başlatmak için

def servis_al(scopes, token_dosyasi):  # Gmail/Calendar servislerinin ortak kullanacağı kimlik doğrulama fonksiyonu
    """Google API için kimlik doğrulaması yapar, gerekirse tarayıcıda izin ister, token'ı dosyaya kaydeder/okur."""
    kimlik = None  # Başta kimlik bilgimiz yok

    if os.path.exists(token_dosyasi):  # Daha önce izin alınmış ve kaydedilmişse
        kimlik = Credentials.from_authorized_user_file(token_dosyasi, scopes)  # Kaydedilmiş token'ı oku

    if not kimlik or not kimlik.valid:  # Token yoksa veya geçersizse (süresi dolmuşsa)
        if kimlik and kimlik.expired and kimlik.refresh_token:  # Süresi dolmuş ama yenileme token'ı varsa
            kimlik.refresh(Request())  # Tekrar tarayıcı açmadan sessizce yenile
        else:  # Hiç izin alınmamışsa
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)  # İndirdiğimiz dosyayı oku
            kimlik = flow.run_local_server(port=0)  # Tarayıcıda izin ekranı aç, kullanıcı onaylayınca token al

        with open(token_dosyasi, "w") as f:  # Alınan token'ı dosyaya kaydet
            f.write(kimlik.to_json())  # Bir dahaki çalıştırmada tekrar tarayıcı açılmasın diye

    return kimlik  # Gmail/Calendar servisini kuracak koda kimliği döndür