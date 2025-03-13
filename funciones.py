import json
import spacy
import random
import speech_recognition as sr
import pyttsx3
from intenciones import intenciones, preguntas 
from num2words import num2words
from fuzzywuzzy import fuzz
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import os
import subprocess

SARA = "Sistema de Asistencia y Respuestas Automatizadas."
DB_FILE = "sara_memoria.json"
PREGUNTAS = "sara_memoria.json"
nlp = spacy.load("en_core_web_md")  # Modelo de lenguaje avanzado

# Objeto de reconocimiento de voz
r = sr.Recognizer()
engine = pyttsx3.init()
mic = sr.Microphone()

keyword = "hola sara" # Palabra clave a detectar
voices = engine.getProperty('voices') # Obtener lista de voces disponibles
r.energy_threshold = 4000 # Establecer un umbral de energía para la detección de silencio
engine.setProperty('rate', 150)  # Ajustar el valor para modificar el tono de la voz

try:  # Seleccionar una voz específica por su índice
    engine.setProperty('voice', voices[2].id)
except IndexError:
    engine.setProperty('voice', voices[0].id)

def detect_keyword(keyword): # Funcion para detectar cuando llaman al asistente
    """Esta funcion escucha lo que se esta hablando a la espera de detectar la palabra clave (Keyword) que activa al asistente."""
    while True:
        print("Escucho...")
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10)

        # usuario = comparar_voces(voz_desconocida, voces_conocidas)

        try:
            # Convertir el audio en texto
            text = r.recognize_google(audio, language="es-ES")
            print("Escuchado:", text)

            # Verificar si se ha pronunciado la palabra clave
            if keyword in text or any(keyword in frases for frases in preguntas.values()):
                print(f"Palabra clave detectada: {keyword}")
                engine.say(f"Hola, ¿En qué te puedo ayudar?")
                engine.runAndWait()
                return True               
            elif text.lower() in keyword.lower():
                print(f"Palabra clave detectada: {keyword}")
                engine.say(f"Hola, ¿En que te puedo ayudar?")
                engine.runAndWait()
                return True
            elif keyword.lower() == detectar_pregunta(text):
                print(f"Palabra clave detectada: {keyword}")
                engine.say(f"Hola, ¿En que te puedo ayudar?")
                engine.runAndWait()
                return True

        except sr.UnknownValueError:
            print("No se pudo reconocer el audio")

def escuchar(): # Funcion para escuchar lo que se habla.
    with mic as source:
        engine.runAndWait()
        print("Te escucho...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=20)
    
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print(f"Se escucho lo siguiente: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
        return ""
    except sr.RequestError:
        engine.say("Error de conexión con el reconocimiento de voz.")
        engine.runAndWait()
        return ""

def listaReproduccion():
    ruta_carpeta_audio = os.path.expanduser("~/Music/Playlists")
    if not os.path.exists(ruta_carpeta_audio):
        return []
    archivos = os.listdir(ruta_carpeta_audio)
    return [os.path.splitext(archivo)[0] for archivo in archivos if archivo.endswith(".xspf")]

def detectar_pregunta(texto): # Función para detectar preguntas y encontrar la pregunta correspondiente
    mejor_pregunta = None
    mejor_similitud = 70

    # Iterar sobre las preguntas y variantes
    for pregunta, variantes in preguntas.items():
        for variante in variantes:
            similitud = fuzz.ratio(texto.lower(), variante.lower())

            # Actualizar la pregunta y similitud si encontramos una mejor coincidencia
            if similitud > mejor_similitud:
                mejor_pregunta = pregunta
                mejor_similitud = similitud

    return mejor_pregunta


"""def detectar_pregunta(texto):
    mejor_pregunta, mejor_similitud = None, 70

    for frase, categoria in intenciones:
        similitud = fuzz.ratio(texto.lower(), frase.lower())
        if similitud > mejor_similitud:
            mejor_pregunta, mejor_similitud = categoria, similitud

    return mejor_pregunta"""

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

"""def detect_keyword(keyword):
    with sr.Microphone() as source:
        print("Escuchando para detectar la palabra clave...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            return any(word in text for word in respuestas.get(keyword, []))
        except sr.UnknownValueError:
            return False"""

def cargar_memoria():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_memoria(memoria):
    with open(DB_FILE, "w") as f:
        json.dump(memoria, f, indent=4)

def encontrar_pregunta_similar(pregunta, memoria):
    preguntas_guardadas = list(memoria.keys())
    if not preguntas_guardadas:
        return None
    
    pregunta_doc = nlp(pregunta)
    mejor_coincidencia = None
    mejor_similitud = 0.7  # Umbral de similitud
    
    for pregunta_guardada in preguntas_guardadas:
        similitud = pregunta_doc.similarity(nlp(pregunta_guardada))
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_coincidencia = pregunta_guardada
    
    return mejor_coincidencia

def responder(pregunta):
    memoria = cargar_memoria()
    pregunta_procesada = pregunta.lower().strip()
    
    pregunta_similar = encontrar_pregunta_similar(pregunta_procesada, memoria)
    if pregunta_similar:
        return random.choice(memoria[pregunta_similar])
    
    engine.say("No sé la respuesta aún. ¿Me enseñas?")
    engine.runAndWait()
    nueva_respuesta = escuchar()
    
    if nueva_respuesta:
        aprender(pregunta_procesada, nueva_respuesta)
        return "¡Gracias! Ahora ya sé la respuesta."
    
    return "Está bien, seguiré aprendiendo."

def aprender(pregunta, respuesta):
    memoria = cargar_memoria()
    pregunta = pregunta.lower().strip()
    
    if pregunta in memoria:
        memoria[pregunta].append(respuesta)
    else:
        memoria[pregunta] = [respuesta]
    
    guardar_memoria(memoria)
    return "¡Entendido! Aprendí la respuesta."

def editar_respuesta(pregunta, nueva_respuesta):
    memoria = cargar_memoria()
    pregunta = pregunta.lower().strip()
    
    if pregunta in memoria:
        memoria[pregunta] = [nueva_respuesta]
        guardar_memoria(memoria)
        return "La respuesta ha sido actualizada."
    return "No tengo registrada esa pregunta."

def aprender_desde_archivo(archivo):
    memoria = cargar_memoria()
    try:
        with open(archivo, "r", encoding="utf-8") as f:  # Forzar UTF-8
            for linea in f:
                partes = linea.strip().split("|", 1)
                if len(partes) == 2:
                    pregunta, respuesta = partes
                    aprender(pregunta, respuesta)
        return "Aprendí desde el archivo exitosamente."
    except FileNotFoundError:
        return "El archivo no fue encontrado."
    except UnicodeDecodeError:
        return "Error de codificación al leer el archivo."

def sugerir_preguntas():
    memoria = cargar_memoria()
    return list(memoria.keys())[:5] if memoria else []

def limpiar_archivo_referencia(archivo="referencia.txt"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        
        memoria = cargar_memoria()
        nuevas_lineas = [linea for linea in lineas if linea.split("|", 1)[0].strip() not in memoria]
        
        with open(archivo, "w", encoding="utf-8") as f:
            f.writelines(nuevas_lineas)
    
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe.")
    except UnicodeDecodeError:
        print(f"Error de codificación al leer {archivo}.")