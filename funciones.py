import speech_recognition as sr
import pyttsx3
from intenciones import intenciones, respuestas
from num2words import num2words
from fuzzywuzzy import fuzz
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import os
import subprocess

SARA = "Sistema de Asistencia y Respuestas Automatizadas."

# Inicializar reconocimiento de voz y síntesis de voz
r = sr.Recognizer()
engine = pyttsx3.init()

r.energy_threshold = 4000
engine.setProperty('rate', 145)
voices = engine.getProperty('voices')
try:
    engine.setProperty('voice', voices[2].id)
except IndexError:
    engine.setProperty('voice', voices[0].id)

def listaReproduccion():
    ruta_carpeta_audio = os.path.expanduser("~/Music/Playlists")
    if not os.path.exists(ruta_carpeta_audio):
        return []
    archivos = os.listdir(ruta_carpeta_audio)
    return [os.path.splitext(archivo)[0] for archivo in archivos if archivo.endswith(".xspf")]

def detectar_pregunta(texto):
    mejor_pregunta, mejor_similitud = None, 50

    for frase, categoria in intenciones:
        similitud = fuzz.ratio(texto.lower(), frase.lower())
        if similitud > mejor_similitud:
            mejor_pregunta, mejor_similitud = categoria, similitud

    return mejor_pregunta

def buscar_y_ejecutar_archivo(nombre_archivo):
    directorios = [os.path.expanduser("~/Music"), os.path.expanduser("~/Music/Playlists")]
    nombre_archivo = f"{nombre_archivo}.xspf"
    for directorio in directorios:
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        if os.path.exists(ruta_archivo):
            try:
                subprocess.run(["vlc", ruta_archivo])
                return
            except FileNotFoundError:
                print("VLC no está instalado o no se encontró.")
    print(f"No se encontró {nombre_archivo}.")

def set_volume(volume):
    for session in AudioUtilities.GetAllSessions():
        session._ctl.QueryInterface(ISimpleAudioVolume).SetMasterVolume(volume, None)

def convertir_numero(palabra):
    try:
        return int(num2words(palabra))
    except:
        return None

def detect_keyword(keyword):
    with sr.Microphone() as source:
        print("Escuchando para detectar la palabra clave...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            return any(word in text for word in respuestas.get(keyword, []))
        except sr.UnknownValueError:
            return False
