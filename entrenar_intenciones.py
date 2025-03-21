import json
import nltk
import random
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Descargar recursos de NLTK
nltk.download('punkt')

# Cargar dataset de intenciones
dataset = {
    "pregunta": [
        "qué es python",
        "cómo funciona sara",
        "por qué el cielo es azul",
        "cuándo es tu cumpleaños",
        "dónde puedo encontrar información",
        "quién eres",
        "cuál es tu función",
        "puedo pedirte ayuda",
        "debería confiar en sara"
    ],
    "comando": [
        "abre chrome",
        "enciende la luz",
        "apaga la computadora",
        "reproduce música",
        "configura el volumen",
        "ejecuta word",
        "inicia el calendario"
    ],
    "saludo": [
        "hola",
        "buen día",
        "qué tal",
        "hey",
        "hola sara"
    ],
    "despedida": [
        "chau",
        "adiós",
        "hasta luego",
        "nos vemos",
        "hasta la próxima"
    ],
    "alago": [
        "gracias",
        "muy bien",
        "me gusta",
        "eres genial",
        "qué bueno",
        "excelente"
    ]
}

# Crear datos de entrenamiento
frases = []
etiquetas = []

for categoria, ejemplos in dataset.items():
    for frase in ejemplos:
        frases.append(frase)
        etiquetas.append(categoria)

# Convertir texto a vectores numéricos
vectorizador = CountVectorizer()
X = vectorizador.fit_transform(frases)
y = etiquetas

# Entrenar modelo de Naive Bayes
modelo = MultinomialNB()
modelo.fit(X, y)

# Guardar el modelo entrenado
with open("modelo_intenciones.pkl", "wb") as f:
    pickle.dump((vectorizador, modelo), f)

print("Modelo entrenado y guardado como 'modelo_intenciones.pkl'")
