import json
import spacy
import random
import speech_recognition as sr
import pyttsx3
from num2words import num2words
from fuzzywuzzy import fuzz
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import os
import subprocess
import webbrowser
import requests
from bs4 import BeautifulSoup
from sympy import false

SARA = "Sistema de Asistencia y Respuestas Automatizadas."
DB_FILE = "sara_memoria.json"
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

def cargar_memoria(): # Funcion para cargar la BBDD con el contenido del archivo JSON.
    """Carga la memora del archivo .json donde se almacenaran las intenciones, preguntas con sus respuestas y las posibles acciones que SARA pueda realizar."""
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"preguntas_respuestas": {}, "intenciones": {}, "acciones": {}}  # Estructura vacía si hay error

def detect_keyword(keyword, umbral_similitud=80):  
    """Escucha hasta detectar la palabra clave con similitud o salir tras varios intentos fallidos, manejando errores.
    Por defecto tiene el maximo de intentos fallidos en 5, y el umbral de similitud en 80 porciento."""  

    while True:
        # Usar la función escuchar para capturar el texto
        texto = escuchar()
        print(texto)
        
        try:  
            # Verificar si la palabra clave está o es similar
            similitud = fuzz.ratio(texto.lower(), keyword.lower())

            if similitud >= umbral_similitud:  
                print(f"Palabra clave detectada con {similitud}% de similitud: {keyword}")  
                engine.say("Hola, ¿En qué te puedo ayudar?")  
                engine.runAndWait()  
                return True  
            else:  
                print(f"No se detectó la palabra clave (Similitud: {similitud}%). Sigo escuchando...")   

        except sr.UnknownValueError:  
            print("No se pudo entender el audio. ¿Podrías repetirlo?")  
            engine.say("No entendí lo que dijiste. ¿Podrías repetirlo?")  
            engine.runAndWait()

        except sr.RequestError:  
            print("Error de conexión con el servicio de reconocimiento de voz.")  
            engine.say("Hubo un problema de conexión con el reconocimiento de voz.")  
            engine.runAndWait()  
            return False 

        except KeyboardInterrupt:  
            print("\nInterrupción manual. Cerrando la escucha.")  
            engine.say("Hasta luego.")  
            engine.runAndWait()  
            return False  

        except Exception as e:  
            print(f"Ocurrió un error inesperado: {e}")  
            engine.say("Ocurrió un error inesperado. Por favor, verifica el sistema.")  
            engine.runAndWait()  
            break

def escuchar(): # Funcion para escuchar lo que se habla.
    """Esta funcion escucha lo que se esta hablando a la espera de detectar la palabra clave para iniciar el asistente o bien realizar una pregunta o una peticion."""
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
    
def listaReproduccion():
    ruta_carpeta_audio = os.path.expanduser("~/Music/Playlists")
    if not os.path.exists(ruta_carpeta_audio):
        return []
    archivos = os.listdir(ruta_carpeta_audio)
    return [os.path.splitext(archivo)[0] for archivo in archivos if archivo.endswith(".xspf")]

def detectar_pregunta(texto, memoria): # Función para detectar preguntas y encontrar la pregunta correspondiente
    """Esta funcion analiza la pregunta realizada y evalua si se encuentra en la base de datos de preguntas predeterminadas para poder dar la mejor respuesta."""
    texto = texto.lower()
    
    for categoria, datos in memoria["preguntas_respuestas"].items():
        if any(pregunta in texto for pregunta in datos["preguntas"]):
            return random.choice(datos["respuestas"])  # Respuesta aleatoria

    return None  # No encontró respuesta

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
    """Esta funcion convierte texto en numeros, solo si el mismo se puede convertir."""
    try:
        return int(num2words(palabra))
    except:
        return None

def guardar_memoria(memoria):
    """Permite guardar lo que SARA aprende para poder utilizarlo luego"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)

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

def buscar_en_internet(pregunta): # Si una pregunta no es encontrada en la base de datos la busca. 
    """En el caso de que el usuario pregunte algo que SARA no sabe lo busca en internet, si lo encuentra devuelve la respuesta, en caso contrario avisa y devuelve un falso para no guardar la respuesta. """
    url = f"https://www.google.com/search?q={pregunta.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        respuesta = soup.find("span").text if soup.find("span") else "No encontré información exacta."
        return respuesta
    else:
        engine.say("No encontré información en la web.")
        return False
    
def responder(texto, memoria): # Funcion para responder preguntas. 
    intencion = identificar_intencion(texto, memoria)  # Detectar intención

    if intencion == "pregunta":  # Si es una pregunta, buscar en la base de datos
        respuesta = detectar_pregunta(texto, memoria)
        if respuesta:
            engine.say(respuesta)
        else:
            engine.say("No tengo una respuesta exacta, pero buscaré en internet.")
            respuesta_web = buscar_en_internet(texto)
            if respuesta_web:
                engine.say(respuesta_web)
                aprender_pregunta(texto, respuesta_web)  # Aprender la respuesta obtenida
    
    elif intencion == "comando":  # Si es un comando, buscar en acciones
        respuesta = ejecutar_accion(texto, memoria)
        engine.say(respuesta)

    elif intencion in memoria["intenciones"]:  # Si es saludo, despedida o alago
        respuestas_aleatorias = {
            "saludo": ["¡Hola! ¿En qué puedo ayudarte?", "Hola, ¿cómo estás?", "¡Buen día! ¿Cómo te sientes hoy?"],
            "despedida": ["Hasta luego, que tengas un gran día.", "Adiós, aquí estaré cuando me necesites.", "Nos vemos pronto."],
            "alago": ["¡Gracias! Estoy aquí para ayudarte.", "Me alegra que pienses eso.", "¡Aprecio tus palabras!", "Gracias, intento hacer lo mejor posible."]
        }
        engine.say(random.choice(respuestas_aleatorias[intencion]))

    else:
        engine.say("No entendí bien lo que dijiste, ¿puedes repetirlo?")
    
    engine.runAndWait()

def aprender(pregunta, respuesta): #Funcion para que SARA aprenda algo nuevo.
    """En el caso de que una pregunta no exista, SARA puede aprender la respuesta de la misma."""
    memoria = cargar_memoria()
    pregunta = pregunta.lower().strip()
    
    if pregunta in memoria:
        memoria[pregunta].append(respuesta)
    else:
        memoria[pregunta] = [respuesta]
    
    guardar_memoria(memoria)
    return "¡Entendido! Aprendí la respuesta."

def editar_respuesta(pregunta, nueva_respuesta): # Edita una respuesta en caso de que sea erronea. 
    """En el caso de que una respuesta sea erronea y se tenga que corregir, se utiliza esta funcion para modificar la respuesta guardada en memoria."""
    memoria = cargar_memoria()
    pregunta = pregunta.lower().strip()
    
    if pregunta in memoria:
        memoria[pregunta] = [nueva_respuesta]
        guardar_memoria(memoria)
        return "La respuesta ha sido actualizada."
    return "No tengo registrada esa pregunta."

def aprender_pregunta(nueva_pregunta, nueva_respuesta): # Funcion para aprender y guardar la respuesta.
    """En el caso de que la pregunta realizada no se encuentre y se brinde una respuesta para ella quedara almacenada en la memoria para que pueda respnder en un futuro lo nuevo que aprendio."""
    memoria = cargar_memoria()
    
    for categoria, datos in memoria["preguntas_respuestas"].items():
        if nueva_pregunta in datos["preguntas"]:
            datos["respuestas"].append(nueva_respuesta)
            guardar_memoria(memoria)
            return "He aprendido una nueva respuesta para esta pregunta."

    memoria["preguntas_respuestas"][nueva_pregunta] = {
        "preguntas": [nueva_pregunta],
        "respuestas": [nueva_respuesta]
    }
    
    guardar_memoria(memoria)
    return "He aprendido una nueva pregunta y su respuesta."

def identificar_intencion(texto, memoria): # Funcion para detectar la intencion del usuario. 
    """Identifica la intencion del usuario, si no es la misma que esta cargada busca coincidencias para que encuentre una similitud a lo solicitado."""
    texto = texto.lower().strip()
    texto_doc = nlp(texto)

    if texto in memoria["intenciones"]:
        return texto

    mejor_intencion = "desconocido"
    mejor_similitud = 0.8  # Aumentamos el umbral para evitar errores

    for categoria, palabras_clave in memoria["intenciones"].items():
        for palabra in palabras_clave:
            palabra_doc = nlp(palabra)
            
            # Evitar error de vectores vacíos
            if not texto_doc.has_vector or not palabra_doc.has_vector:
                continue

            similitud = texto_doc.similarity(palabra_doc)

            if similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_intencion = categoria
    
    return mejor_intencion

def ejecutar_accion(texto, memoria): # Ejecutar una accion en caso de que SARA lo detecte.
    """Se le puede pedir a SARA que ejecute algun comando predeterminado, con esta funcion ella lo ejecutara."""
   
    for accion, datos in memoria.get("acciones", {}).items():
        if any(comando in texto for comando in datos["comandos"]):
            try:
                subprocess.Popen(datos["ejecutar"])  # Ejecuta la acción
                return f"Ejecutando {accion}..."
            except Exception as e:
                return f"No pude ejecutar {accion}: {e}"

    return "No tengo una acción programada para eso."

