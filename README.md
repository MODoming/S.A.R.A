# SARA - Sistema de Asistencia y Respuestas Automatizadas

SARA es un asistente de voz para Windows desarrollado en Python, capaz de reconocer comandos de voz y responder a preguntas mediante síntesis de voz.

## 📌 Características
- Reconocimiento de voz con `speech_recognition`
- Respuestas habladas con `pyttsx3`
- Detección de palabras clave para activar el asistente
- Reproducción de música desde listas de reproducción
- Control de volumen del sistema
- Consulta de eventos en el calendario con Google Calendar
- Comandos para apagar la computadora
- Base de datos de intenciones para mejorar el reconocimiento de preguntas

## 🛠️ Requisitos
Antes de ejecutar SARA, asegúrate de tener instaladas las siguientes dependencias:
- speechrecognition
- pyttsx3
- fuzzywuzzy
- num2words
- pycaw
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client

Para ello utilice el siguiente comando:

```bash
pip install -r requirements.txt

```

Además, asegúrate de tener instalado [VLC Media Player](https://www.videolan.org/) si deseas utilizar la función de reproducción de música.

### 🔑 Configuración de Google Calendar
Para que SARA pueda acceder a tu calendario de Google, debes generar credenciales:
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Habilita la API de Google Calendar.
3. Crea credenciales de OAuth 2.0 y descarga el archivo `credentials.json`.
4. Guarda `credentials.json` en la carpeta del proyecto.
5. La primera vez que ejecutes SARA, se generará automáticamente `token.json` tras autenticarte.

## 🚀 Instalación y ejecución
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/sara-assistant.git
   cd sara-assistant
   ```
2. Ejecuta el programa:
   ```bash
   python sara_launcher.py
   ```

## 📂 Estructura del proyecto
```
📁 sara-assistant
├── 📄 inicio.py          # Módulo principal del asistente
├── 📄 funciones.py       # Funciones auxiliares del asistente
├── 📄 intenciones.py     # Diccionario de respuestas y base de datos de intenciones
├── 📄 calendario.py      # Módulo de integración con Google Calendar
├── 📄 sara_launcher.py   # Script para iniciar el asistente
├── 📄 credentials.json   # Credenciales de Google Calendar (NO compartir)
├── 📄 token.json         # Token de autenticación de Google Calendar
├── 📄 README.md          # Documentación del proyecto
```

## 📝 Uso
- Di "Hola SARA" para activar el asistente.
- Pregunta "¿Quién eres?" o "¿Qué puedes hacer?" para obtener información sobre sus capacidades.
- Solicita "Escuchar música" para reproducir listas de reproducción guardadas.
- Ajusta el volumen diciendo "Subir volumen" o "Bajar volumen".
- Apaga la computadora con "Apagar la computadora".
- Consulta tu calendario con "Muestra mi calendario" o "¿Tengo eventos hoy?".

## 📊 Base de datos de intenciones
El módulo `intenciones.py` ahora centraliza todas las frases y respuestas para mejorar el reconocimiento de preguntas. Esto ayuda a SARA a identificar mejor las intenciones del usuario y mejorar sus respuestas.

## ⚡ Contribuciones
Si deseas mejorar SARA, ¡eres bienvenido! Puedes hacer un fork del repositorio y enviar un pull request con tus mejoras.

## 📜 Licencia
Este proyecto está bajo la licencia MIT.

