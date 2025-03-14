import json
import spacy
import random
import speech_recognition as sr
import pyttsx3
from intenciones import INTENCIONES, preguntas, ACCIONES
from num2words import num2words
from fuzzywuzzy import fuzz
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import os
import subprocess

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

def cargar_preguntas():
    """Carga las preguntas desde un archivo JSON."""
    try:
        with open("sara_preguntas.json", "r", encoding="utf-8") as file:
            preguntas = json.load(file)
            print("Preguntas cargadas correctamente.")
            return preguntas
    except Exception as e:
        print(f"Error al cargar las preguntas: {e}")
        return {}

PREGUNTAS = cargar_preguntas()

def detect_keyword(keyword, max_intentos=5, umbral_similitud=80):  
    """Escucha hasta detectar la palabra clave con similitud o salir tras varios intentos fallidos, manejando errores.
    Por defecto tiene el maximo de intentos fallidos en 5, y el umbral de similitud en 80 porciento."""  
    intentos = 0  

    while intentos < max_intentos:  
        print(f"Escuchando... (Intento {intentos + 1}/{max_intentos})")  
        
        try:  
            # Usar la función escuchar para capturar el texto
            texto = escuchar()
            
            if not texto:  
                intentos += 1  
                print("No se detectó audio o no se entendió el mensaje.")  
                continue  # Si no se entendió nada, seguir escuchando

            # Verificar si la palabra clave está o es similar
            similitud = fuzz.ratio(texto.lower(), keyword.lower())

            if similitud >= umbral_similitud:  
                print(f"Palabra clave detectada con {similitud}% de similitud: {keyword}")  
                engine.say("Hola, ¿En qué te puedo ayudar?")  
                engine.runAndWait()  
                return True  
            else:  
                print(f"No se detectó la palabra clave (Similitud: {similitud}%). Sigo escuchando...")  
                intentos += 1  

        except sr.UnknownValueError:  
            print("No se pudo entender el audio. ¿Podrías repetirlo?")  
            engine.say("No entendí lo que dijiste. ¿Podrías repetirlo?")  
            engine.runAndWait()  
            intentos += 1  

        except sr.RequestError:  
            print("Error de conexión con el servicio de reconocimiento de voz.")  
            engine.say("Hubo un problema de conexión con el reconocimiento de voz.")  
            engine.runAndWait()  
            break

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

    # Si alcanza el máximo de intentos o hay un fallo grave
    print("No se detectó la palabra clave o hubo un problema. Finalizando escucha.")  
    engine.say("No detecté la palabra clave o hubo un problema. Finalizando escucha.")  
    engine.runAndWait()  
    return False

def escuchar(timeout=20, language="es-ES"): # Funcion para escuchar lo que se habla.
    """Esta funcion escucha lo que se esta hablando a la espera de detectar la palabra clave para iniciar el asistente o bien realizar una pregunta o una peticion.
    Por defecto mantiene 20 segundos de espera para escuchar el audio y el idioma es español."""
    with mic as source:
        engine.runAndWait()
        print("Te escucho...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout)
    
    try:
        texto = r.recognize_google(audio, language)
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

def detectar_pregunta(texto, mejor_similitud=70): # Función para detectar preguntas y encontrar la pregunta correspondiente
    """Esta funcion analiza la pregunta realizada y evalua si se encuentra en la base de datos de preguntas predeterminadas para poder dar la mejor respuesta.
    Mantiene la similitud del 70 porciento a no ser que se ingrese otro porcentaje."""
    mejor_pregunta = None    

    # Iterar sobre las preguntas y variantes
    for pregunta, variantes in PREGUNTAS.items():
        for variante in variantes:
            similitud = fuzz.ratio(texto.lower(), variante.lower())

            # Actualizar la pregunta y similitud si encontramos una mejor coincidencia
            if similitud > mejor_similitud:
                mejor_pregunta = pregunta
                mejor_similitud = similitud

    return mejor_pregunta, mejor_similitud

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

"""def sugerir_preguntas():
    memoria = cargar_memoria()
    return list(memoria.keys())[:5] if memoria else []"""

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

def detectar_intencion(comando, umbral_similitud=60):
    """Detectar la intención de la frase (pregunta, comando, saludo, etc.)."""
    mejor_intencion = None
    mejor_similitud = 0

    # Buscar la intención más cercana
    for intencion, palabras in INTENCIONES.items():
        for palabra in palabras:
            similitud = fuzz.ratio(comando.lower(), palabra.lower())

            if similitud > mejor_similitud and similitud >= umbral_similitud:
                mejor_similitud = similitud
                mejor_intencion = intencion

    return mejor_intencion

def analizar_texto(texto):
    """Analiza el texto con spaCy para extraer entidades y estructura."""
    doc = nlp(texto)

    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    verbos = [token.text for token in doc if token.pos_ == "VERB"]
    preguntas = [token.text for token in doc if token.tag_ == "PRON-INT"]

    return {"entidades": entidades, "verbos": verbos, "preguntas": preguntas}

def detectar_intencion_spacy(comando):
    """Detecta la intención usando spaCy (pregunta, comando o saludo)."""
    analisis = analizar_texto(comando)

    if analisis["preguntas"]:
        return "pregunta"
    elif analisis["verbos"]:
        return "comando"
    else:
        return "otro"
    
def procesar_comando_spacy(comando):
    """Procesa el comando según la intención detectada con spaCy."""
    intencion = detectar_intencion_spacy(comando)

    if intencion == "pregunta":
        respuesta = detectar_pregunta(comando)
        if respuesta:
            engine.say(respuesta)
        else:
            engine.say("No tengo una respuesta para esa pregunta.")
    
    elif intencion == "comando":
        accion = detectar_accion(comando)
        if accion:
            ejecutar_accion(accion)
        else:
            engine.say("No conozco ese comando, ¿quieres probar otra cosa?")
    
    else:
        engine.say("No entendí bien lo que dijiste, ¿podrías repetirlo?")

    engine.runAndWait()

def detectar_accion(comando):  
    """Detectar si el comando coincide con alguna acción conocida."""
    mejor_accion = None  
    mejor_similitud = 70  

    for accion, variantes in ACCIONES.items():  
        for variante in variantes:  
            similitud = fuzz.ratio(comando.lower(), variante.lower())  

            if similitud > mejor_similitud:  
                mejor_accion = accion  
                mejor_similitud = similitud  

    return mejor_accion

def ejecutar_accion(accion):  
    """Ejecutar la función correspondiente a la acción detectada."""
    if accion == "Abrir navegador":  
        print("Esto es una accion")  
    elif accion == "Reproducir música":  
        listaReproduccion()  
    elif accion == "Cerrar sesión":  
        print("Esta es para cerrar la cumptadora")
    elif accion == "Bloquear pantalla":  
        print("pantalla")
    else:  
        engine.say("No conozco esa acción, ¿podrías repetirlo?")  
        engine.runAndWait()