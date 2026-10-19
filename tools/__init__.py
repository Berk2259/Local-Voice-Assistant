from .zaman import saat_getir
from .notlar import not_ekle, notlari_listele
from .uygulama import uygulama_ac
from .mail import son_mailleri_getir
from .takvim import etkinlik_ekle, yaklasan_etkinlikler

ARACLAR = {
    "saat_getir": saat_getir,
    "not_ekle": not_ekle,
    "notlari_listele": notlari_listele,
    "uygulama_ac": uygulama_ac,
    "son_mailleri_getir": son_mailleri_getir,
    "etkinlik_ekle": etkinlik_ekle,
    "yaklasan_etkinlikler": yaklasan_etkinlikler,
}