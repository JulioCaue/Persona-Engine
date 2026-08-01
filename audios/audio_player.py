import scipy.io.wavfile as wav
import sounddevice as sd
import os
from logs import log_writer

def Tocar_Wav():
    "Toca um arquivo wav"
    local_arquivo_output = "audios/audio_output.wav"
    if os.path.exists(local_arquivo_output):
        try:
            sample_rate,data = wav.read(local_arquivo_output)
            sd.play(data,sample_rate)
        except Exception as e:
            log_writer.write(__name__,f"Ocorreu um erro ao tocar wav: {e}")