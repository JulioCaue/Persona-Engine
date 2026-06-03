import speech_recognition as sr
from groq import Groq as grq
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()

GROQ_API_KEY=os.getenv('GROQ_API_KEY')

def criar_wav():
    recognizer = sr.Recognizer()
    TIMEOUT_AUDIO = 5
    TEMPO_MAXIMO_FALA = 30
    try:
        with sr.Microphone() as mic:
            recognizer.pause_threshold=2
            recognizer.energy_threshold=100
            try:
                audio_data = recognizer.listen(mic,TIMEOUT_AUDIO,TEMPO_MAXIMO_FALA)

                wav_bytes = audio_data.get_wav_data()

                with open("audio_output.wav","wb") as file:
                    file.write(wav_bytes)

                print(f"arquivo criado. Threshold foi: {recognizer.energy_threshold}")
            except Exception as e:
                print(f"Um erro ocorreu: {e}\nThreshold foi: {recognizer.energy_threshold}")
                

    except sr.WaitTimeoutError:
        pass

    except sr.UnknownValueError:
        pass


def receber_STT():
    #Inicia cliente groq
    client = grq(api_key=GROQ_API_KEY,timeout=5)

    #Caminho pro arquivo de audio
    filename = os.path.dirname(__file__) + "/audio_output.wav" # nome do arquivo

    # Open the audio file
    with open(filename, "rb") as file:
        #Criar Transcriçao
        transcription = client.audio.transcriptions.create(
        file=file, # Arquivo de audio
        model="whisper-large-v3-turbo", # Modelo para transcricao
        )
        language="pt-BR"
        return transcription.text

def pegar_transcricao():
    criar_wav()
    return receber_STT()