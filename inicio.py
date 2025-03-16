import speech_recognition as sr
import pyttsx3
import time
from funciones import *


SARA = "Sistema de Asistencia y Respuestas Automatizadas."
DB_FILE = "sara_memoria.json"
TIEMPO_ESPERA = 20  # Segundos antes de volver a requerir "Hola SARA"


# Inicializar reconocimiento de voz y síntesis de voz
r = sr.Recognizer()
engine = pyttsx3.init()
mic = sr.Microphone()

keyword = "hola sara"
voices = engine.getProperty('voices')

# Manejar selección de voz con validación
try:
    engine.setProperty('voice', voices[2].id)
except IndexError:
    engine.setProperty('voice', voices[0].id)  # Usar la primera voz disponible

r.energy_threshold = 4000
engine.setProperty('rate', 150)
memoria = cargar_memoria()

"""def responder(texto, memoria):

    intencion = identificar_intencion(texto)  # Detectar intención

    if intencion == "pregunta":  # Si es una pregunta, buscar en la base de datos
        respuesta = detectar_pregunta(texto, memoria)
        if respuesta:
            engine.say(respuesta)
        else:
            engine.say("No tengo una respuesta exacta, pero puedo buscar en internet.")
            webbrowser.open(f"https://www.google.com/search?q={texto.replace(' ', '+')}")

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
"""


while True:
    if detect_keyword(keyword):
        tiempo_inicio = time.time()  # Guarda el tiempo en que SARA fue activada
        
        while time.time() - tiempo_inicio < TIEMPO_ESPERA:
            with sr.Microphone() as source:
                comando = escuchar()
                if comando:
                    try:
                        responder(comando, memoria)
                        tiempo_inicio = time.time()  # Reinicia el contador si el usuario sigue hablando
                    except Exception as e:
                        print(f"Error en responder(): {e}")  # Muestra el error exacto en la terminal
                        engine.say("Hubo un error interno, por favor intenta de nuevo.")
                        engine.runAndWait()
