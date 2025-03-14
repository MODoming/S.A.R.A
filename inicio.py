import speech_recognition as sr
import pyttsx3
import os
from funciones import *
from Calendario import *
from intenciones import *  # Importar respuestas correctamente

SARA = "Sistema de Asistencia y Respuestas Automatizadas."
DB_FILE = "sara_memoria.json"
referencia = "referencia.txt"

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

# Aprender desde archivo referencia.txt al inicio
"""if os.path.exists(referencia):
    aprender_desde_archivo(referencia)
    limpiar_archivo_referencia(referencia)"""

"""def respuesta(texto):
    print(f"Usuario: {texto}")
    pregunta = detectar_pregunta(texto)
    
    if pregunta in preguntas:
        engine.say(preguntas[pregunta])

    elif pregunta == "Escuchar música":
        reproducir = listaReproduccion()
        engine.say(f"Las siguientes listas están para ser escuchadas. {', '.join(reproducir)}. Elige una")
        engine.runAndWait()
        lista = escuchar()
        if lista:
            buscar_y_ejecutar_archivo(lista)
        else:
            engine.say("No puedo encontrar esa lista.")

    elif pregunta == "Volumen":
        engine.say("Dime el porcentaje de audio que quieres")
        engine.runAndWait()
        volumen_texto = escuchar()
        try:
            volumen = float(volumen_texto) / 100 if volumen_texto.isdigit() else int(convertir_numero(volumen_texto)) / 100
            set_volume(volumen)
        except ValueError:
            engine.say("Formato de volumen no válido. Intenta de nuevo.")

    elif pregunta == "Apagar":
        engine.say("¿Estás seguro que quieres apagar la computadora?")
        engine.runAndWait()
        respuesta = escuchar().lower()
        if respuesta in ["si", "sí"]:
            engine.say("La computadora se va a apagar. Hasta la próxima.")
            os.system("shutdown -s -t 30")
        else:
            engine.say("La computadora no se apagará. Gracias por confirmar.")

    elif pregunta == "Calendario":
        eventos = obtener_eventos()
        if eventos:
            engine.say("Estos son tus próximos eventos: " + ", ".join(eventos))
        else:
            engine.say("No tienes eventos programados.")
        engine.runAndWait()

    elif pregunta == "Crear evento":
        engine.say("Dime el título del evento.")
        engine.runAndWait()
        titulo = escuchar()

        engine.say("Dime una breve descripción.")
        engine.runAndWait()
        descripcion = escuchar()

        engine.say("Dime la fecha y hora de inicio en formato 'día mes año hora minutos'.")
        engine.runAndWait()
        fecha_inicio_texto = escuchar()

        engine.say("Dime la fecha y hora de finalización.")
        engine.runAndWait()
        fecha_fin_texto = escuchar()

        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_texto, "%d %m %Y %H %M")
            fecha_fin = datetime.datetime.strptime(fecha_fin_texto, "%d %m %Y %H %M")
            link = crear_evento(titulo, descripcion, fecha_inicio, fecha_fin)
            if link:
                engine.say(f"Evento creado correctamente. Puedes verlo aquí: {link}")
            else:
                engine.say("Hubo un problema al crear el evento.")
        except ValueError:
            engine.say("Formato de fecha incorrecto. Intenta de nuevo.")        
        engine.runAndWait()

    else:
        respuesta_nlp = responder(texto)
        engine.say(respuesta_nlp)
        if respuesta_nlp == "No sé la respuesta aún. ¿Me enseñas?":
            engine.runAndWait()
            nueva_respuesta = escuchar()
            if nueva_respuesta:
                aprender(texto, nueva_respuesta)
                engine.say("Gracias, ahora lo recordaré.")
    
    engine.runAndWait()"""

while detect_keyword(keyword):
    with sr.Microphone() as source:
        comando = escuchar()
        if comando:
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
                    engine.say("No entendí el comando, ¿puedes repetirlo?")
            
            else:
                engine.say("No entendí bien lo que dijiste, ¿podrías repetirlo?")

            engine.runAndWait()
