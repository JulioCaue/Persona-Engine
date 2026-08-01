import scipy.io.wavfile as wav
import sounddevice as sd
from logs import log_writer


def Tocar_Wav():
    "Toca um arquivo wav"
    try:
        sample_rate,data = wav.read("audios/audio_output.wav")
        sd.play(data,sample_rate)
    except Exception as e:
        log_writer.write(f"Ocorreu um erro ao tocar wav: {e}")