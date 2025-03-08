import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configurar alcance y archivo de credenciales
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def obtener_credenciales():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def obtener_eventos():
    creds = obtener_credenciales()
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    try:
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No se encontraron eventos próximos.')
            return []

        eventos_lista = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            eventos_lista.append(f"{event['summary']} - {start}")
            print(eventos_lista[-1])
        return eventos_lista
    except Exception as e:
        print(f"Error al obtener eventos: {e}")
        return []

def crear_evento(titulo, descripcion, inicio, fin, zona_horaria='Europe/Madrid'):
    creds = obtener_credenciales()
    service = build('calendar', 'v3', credentials=creds)
    
    evento = {
        'summary': titulo,
        'description': descripcion,
        'start': {'dateTime': inicio.isoformat(), 'timeZone': zona_horaria},
        'end': {'dateTime': fin.isoformat(), 'timeZone': zona_horaria},
    }
    
    try:
        evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
        print(f'Evento creado: {evento_creado.get("htmlLink")}')
        return evento_creado.get("htmlLink")
    except Exception as e:
        print(f"Error al crear evento: {e}")
        return None

if __name__ == '__main__':
    obtener_eventos()
