import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from piper import PiperVoice

SURE = 5
ORNEKLEME_HIZI = 16000

_model = WhisperModel("small", device="cpu", compute_type="int8")

def dinle() -> str:
    """Mikrofondan SURE saniye kayıt alır, metne çevirip döndürür."""
    print(f"{SURE} saniye boyunca konuş...")
    kayit = sd.rec(int(SURE * ORNEKLEME_HIZI), samplerate=ORNEKLEME_HIZI, channels=1, dtype="float32")
    sd.wait()

    audio = kayit.flatten()
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