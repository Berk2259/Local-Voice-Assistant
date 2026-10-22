import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from piper import PiperVoice
from openwakeword.model import Model as WakeWordModel

SURE = 5
ORNEKLEME_HIZI = 16000

_model = WhisperModel("small", device="cpu", compute_type="int8")
_wakeword_modeli = WakeWordModel(wakeword_models=["hey_jarvis"])

def uyandirma_kelimesi_bekle(esik: float = 0.5) -> None:
    """'Hey Jarvis' duyulana kadar sürekli dinler, duyunca döner."""
    PENCERE = 1280
    with sd.InputStream(samplerate=16000, channels=1, dtype="int16") as stream:
        while True:
            audio_chunk, _ = stream.read(PENCERE)
            audio_chunk = audio_chunk.flatten()
            prediction = _wakeword_modeli.predict(audio_chunk)
            if prediction.get("hey_jarvis", 0) > esik:
                _wakeword_modeli.reset()  # aynı tetiklemenin tekrar sayılmaması için
                return

PENCERE_SURESI = 0.03  # her parçanın süresi (saniye)
PENCERE = int(ORNEKLEME_HIZI * PENCERE_SURESI)
SES_ESIGI = 0.02  # bu seviyenin üstü "konuşma" sayılır
SESSIZLIK_SINIRI = 1.2  # bu kadar saniye sessizlik olursa dur
MAKS_SURE = 15  # güvenlik için üst sınır (saniye)

def dinle() -> str:
    """Konuşma başlayınca kayda başlar, sessizlik algılanınca durur, metne çevirip döndürür."""
    print("Dinliyorum...")

    parcalar = []
    konusma_basladi = False
    sessiz_parca_sayisi = 0
    sessizlik_limiti = int(SESSIZLIK_SINIRI / PENCERE_SURESI)
    maks_parca_sayisi = int(MAKS_SURE / PENCERE_SURESI)

    with sd.InputStream(samplerate=ORNEKLEME_HIZI, channels=1, dtype="float32") as stream:
        for _ in range(maks_parca_sayisi):
            parca, _ = stream.read(PENCERE)
            parca = parca.flatten()
            enerji = np.sqrt(np.mean(parca ** 2))

            if enerji > SES_ESIGI:
                konusma_basladi = True
                sessiz_parca_sayisi = 0
                parcalar.append(parca)
            elif konusma_basladi:
                sessiz_parca_sayisi += 1
                parcalar.append(parca)
                if sessiz_parca_sayisi > sessizlik_limiti:
                    break

    if not parcalar:
        return ""

    audio = np.concatenate(parcalar)
    segments, _ = _model.transcribe(audio, language="tr")
    return " ".join(segment.text for segment in segments).strip()

_ses_modeli = PiperVoice.load("voices/tr_TR-dfki-medium.onnx")

def konus(metin: str) -> None:
    """Verilen metni Türkçe TTS ile sese çevirip hoparlörden çalar."""
    for parca in _ses_modeli.synthesize(metin):
        sd.play(parca.audio_float_array, samplerate=parca.sample_rate)
        sd.wait()

if __name__ == "__main__":
    konus("Merhaba, ben senin sesli asistanın.")