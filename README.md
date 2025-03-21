# SARA - Sistema de Asistencia y Respuestas Automatizadas

SARA es un asistente de voz para Windows desarrollado en Python, capaz de reconocer comandos de voz, responder preguntas mediante síntesis de voz y aprender de nuevas interacciones utilizando inteligencia artificial.

## Presentación del Proyecto: S.A.R.A.

Estoy desarrollando SARA, un proyecto inicial con el objetivo de aprender y experimentar con inteligencia artificial de manera autodidacta. SARA es un sistema de asistencia automatizada que utiliza IA para brindar respuestas a los usuarios, ejecutar comandos en el sistema y realizar recomendaciones personalizadas para mejorar la experiencia de interacción digital.

Este proyecto está en constante evolución, y se le irán agregando nuevas funcionalidades a medida que aprenda y se optimice.

# Características iniciales del proyecto:
* **Asistencia automatizada**: SARA ofrece respuestas a preguntas comunes mediante procesamiento de lenguaje natural.
* **Aprendizaje continuo**: SARA puede aprender nuevas preguntas y respuestas en tiempo real, almacenándolas en su base de datos para futuras interacciones.
* **Ejecución de comandos en Windows**: Puede abrir aplicaciones, gestionar archivos, controlar volumen, y ejecutar tareas del sistema.
* **Integración con Google Calendar**: Permite consultar eventos y gestionar el calendario.
* **Búsqueda en Internet**: Si no encuentra una respuesta en su base de datos, puede buscarla en Google y aprender de la información encontrada.
* **Reconocimiento de intenciones**: Identifica si el usuario hace una pregunta, da un comando o emite un saludo, despedida o alago.

Este proyecto es una excelente oportunidad para seguir aprendiendo sobre IA mientras construyo una herramienta útil con múltiples aplicaciones.

## 📌 Características
- Reconocimiento de voz con `speech_recognition`
- Respuestas habladas con `pyttsx3`
- Detección de palabras clave para activar el asistente
- Aprendizaje de nuevas preguntas y respuestas dinámicamente
- Ejecución de acciones en Windows (abrir aplicaciones, apagar PC, gestionar archivos, etc.)
- Integración con Google Calendar
- Búsqueda automática de información en Internet si la respuesta no está en la base de datos

## 🛠️ Requisitos
Antes de ejecutar SARA, asegúrate de tener instaladas las siguientes dependencias:
- speechrecognition
- pyttsx3
- spacy
- beautifulsoup4
- requests
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client

Para instalarlas, ejecuta el siguiente comando:

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
   python inicio.py
   ```

## 📂 Estructura del proyecto
```
📁 sara-assistant
├── 📄 inicio.py          # Módulo principal del asistente
├── 📄 funciones.py       # Funciones auxiliares del asistente
├── 📄 intenciones.py     # Diccionario de respuestas y base de datos de intenciones
├── 📄 calendario.py      # Módulo de integración con Google Calendar
├── 📄 sara_memoria.json  # Base de datos de preguntas, respuestas y acciones
├── 📄 credentials.json   # Credenciales de Google Calendar (NO compartido)
├── 📄 token.json         # Token de autenticación de Google Calendar (NO compartido)
├── 📄 README.md          # Documentación del proyecto
```

## 📝 Uso
- Di "Hola SARA" para activar el asistente.
- Pregunta "¿Quién eres?" o "¿Qué puedes hacer?" para obtener información sobre sus capacidades.
- Pregunta cualquier cosa, y si no conoce la respuesta, la buscará en internet y la aprenderá.
- Solicita "Abrir Chrome" o "Abrir calculadora" para ejecutar aplicaciones.
- Ajusta el volumen diciendo "Subir volumen" o "Bajar volumen".
- Apaga la computadora con "Apagar la computadora".
- Consulta tu calendario con "Muestra mi calendario" o "¿Tengo eventos hoy?".

## 📊 Base de datos de intenciones
El módulo `sara_memoria.json` ahora almacena todas las preguntas, respuestas y comandos de SARA. Esto le permite aprender dinámicamente y mejorar su precisión en la detección de intenciones.

## 🔮 Futuras mejoras
Planeo seguir mejorando SARA con las siguientes características:
- **Mayor integración con IA:** Implementar modelos más avanzados para mejorar el procesamiento del lenguaje natural.
- **Compatibilidad con más aplicaciones:** Agregar integración con plataformas como Spotify, WhatsApp y asistentes de correo.
- **Interacción contextual:** Mejorar la capacidad de recordar el contexto de la conversación.
- **Respuestas más naturales:** Implementar generadores de texto para hacer que las respuestas sean más fluidas y humanas.
- **Mejora en la ejecución de tareas:** Agregar la posibilidad de automatizar flujos de trabajo en el sistema.

## Mejoras Recientes (última versión)
1. **Desarrollo Autonómico de Respuestas:**  
   SARA ahora puede generar respuestas de manera autónoma, mejorando con el tiempo gracias al uso de técnicas de procesamiento de lenguaje natural (NLP).

2. **Independencia de Internet:**  
   El proyecto ha sido optimizado para funcionar sin necesidad de una conexión a internet, permitiendo que SARA opere localmente y mantenga su funcionalidad sin depender de servicios externos.

3. **Enfoque Progresivo de Aprendizaje:**  
   SARA aprenderá progresivamente mediante el análisis de interacciones previas, lo que permite que sus respuestas se vuelvan cada vez más precisas y contextuales.

4. **Integración de Modelos Avanzados de IA:**  
   En el futuro, se planea integrar modelos más avanzados de IA para mejorar la capacidad de respuesta y la comprensión contextual de SARA.

## Objetivos Futuros
- Mejorar la precisión y rapidez de las respuestas mediante la integración de modelos de lenguaje más complejos.
- Crear una interfaz de usuario que facilite la interacción con SARA.
- Expandir las capacidades de SARA para realizar tareas más complejas de manera autónoma.


## ⚡ Contribuciones
Si deseas mejorar SARA, ¡eres bienvenido! Puedes hacer un fork del repositorio y enviar un pull request con tus mejoras.

## 📜 Licencia
Este proyecto está bajo la licencia MIT.
