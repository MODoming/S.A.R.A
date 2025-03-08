from importlib.metadata import version, PackageNotFoundError

dependencias = ["speechrecognition", "pyttsx3", "fuzzywuzzy", "num2words", "pycaw", "datetime", "os.path", "google.oauth2.credentials", "google_auth_oauthlib.flow", "googleapiclient.discovery", ""]

for paquete in dependencias:
    try:
        print(f"{paquete}: {version(paquete)}")
    except PackageNotFoundError:
        print(f"{paquete} no está instalado")