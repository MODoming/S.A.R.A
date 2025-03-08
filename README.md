# SARA - Sistema de Asistencia y Respuestas Automatizadas

SARA es un asistente de voz para Windows desarrollado en Python, capaz de reconocer comandos de voz y responder a preguntas mediante síntesis de voz.

## Presentación del Proyecto: S.A.R.A.

Estoy desarrollando SARA, un proyecto inicial que tiene como objetivo aprender y experimentar con inteligencia artificial de manera autodidacta. SARA es un sistema de asistencia automatizada que utiliza IA para brindar respuestas a los usuarios y realizar recomendaciones personalizadas, con el fin de mejorar la experiencia de interacción digital.

Este proyecto está en sus primeras fases, y poco a poco iré agregando nuevas funcionalidades y habilidades. La idea es desarrollar una plataforma que sea capaz de asistir a los usuarios de manera eficiente, adaptándose a sus consultas y ofreciendo recomendaciones útiles basadas en su comportamiento e interacción con el sistema.

# Características iniciales del proyecto:
* Asistencia automatizada: SARA ofrece respuestas iniciales a preguntas comunes, utilizando procesamiento de lenguaje natural para interpretar las consultas.
* Recomendaciones personalizadas: Aunque en sus primeras fases, el sistema busca brindar sugerencias basadas en el contexto de las interacciones.
* Aprendizaje continuo: El sistema mejora con el tiempo mediante el aprendizaje de interacciones pasadas, permitiendo que se ajuste a las necesidades de los usuarios.
* Desarrollo progresivo: Actualmente, el proyecto está en desarrollo y en el futuro se agregarán más funciones y capacidades a medida que aprenda y perfeccione sus habilidades.

Este proyecto es una excelente oportunidad para seguir aprendiendo sobre IA, mientras construyo una herramienta útil que podría aplicarse a distintos ámbitos en el futuro. Mi objetivo es que SARA evolucione de manera orgánica, agregando valor tanto a mi aprendizaje como a posibles implementaciones futuras.

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

