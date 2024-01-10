import speech_recognition as sr
import pyttsx3 as pyt
import os
from time import sleep
from gtts import gTTS
import openai

# Gunakan variabel lingkungan untuk menyimpan kunci API
openai.api_key = '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'

engine = pyt.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def salam():
    file_path = os.path.dirname(os.path.abspath(__file__))
    halo = os.path.join(file_path, 'bank_voice', 'halo.mp3')
    os.system(f'start {halo}')
    print('Halo, saya Michelle. Katakan sesuatu.')
    sleep(3)

def perintah():
    mendengar = sr.Recognizer()
    with sr.Microphone() as source:
        print('Mendengarkan....')
        try:
            suara = mendengar.listen(source, phrase_time_limit=5)
            print('Diterima...')
            dengar = mendengar.recognize_google(suara, language='id-ID')
            print(dengar)
        except sr.UnknownValueError:
            print('Maaf, tidak dapat mengenali suara. Silakan coba lagi.')
            return ""
        except sr.RequestError:
            print('Terjadi kesalahan pada koneksi suara. Periksa koneksi internet Anda.')
            return ""
        return dengar

def text_to_speech(text):
    tts = gTTS(text=text, lang='id')
    try:
        tts.save("output.mp3")
        os.system(f'start output.mp3')
    except Exception as e:
        print(f'Error: {e}')

def run_michelle():
    Layanan = perintah()
    if not Layanan:
        return  # Keluar dari fungsi jika terjadi kesalahan pada pengenalan suara

    if 'keluar' in Layanan or 'tutup' in Layanan:
        file_path = os.path.dirname(os.path.abspath(__file__))
        keluar = os.path.join(file_path, 'bank_voice', 'keluar.mp3')
        os.system(f'start {keluar}')
        print('Sampai jumpa lagi, terima kasih..')
        sleep(4)
        exit()
    else:
        responsegpt = openai.Completion.create(
            engine='gpt-3.5-turbo-instruct',
            prompt=Layanan,
            max_tokens=200
        )

        answergpt = responsegpt.choices[0].text.strip()
        print(answergpt)
        text_to_speech(answergpt)

        print(Layanan)

while True:
    salam()
    run_michelle()
