import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Portées (scopes) demandées à l'utilisateur
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def get_gmail_service():
    """
    Récupère un service Gmail API authentifié.
    Gère automatiquement le fichier token.json pour stocker les tokens.
    """
    creds = None
    
    # Le fichier token.json stocke les tokens d'accès et de rafraîchissement
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # S'il n'y a pas de token valide, on lance le flow OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8081)
        # Sauvegarde les tokens pour la prochaine fois
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def send_email(to: str, subject: str, body_html: str) -> bool:
    """
    Envoie un email en utilisant l'API Gmail.
    
    Args:
        to: Adresse email du destinataire
        subject: Objet de l'email
        body_html: Corps du message en format HTML
    
    Returns:
        True si l'envoi a réussi, False sinon
    """
    service = get_gmail_service()
    
    # Créer le message
    message = MIMEText(body_html, 'html')
    message['to'] = to
    message['subject'] = subject
    # L'expéditeur est automatiquement "me" (l'utilisateur authentifié)
    
    # Encoder le message en base64 URL-safe (exigé par l'API Gmail)
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    # Construire le corps de la requête
    create_message = {'raw': encoded_message}
    
    try:
        sent_message = service.users().messages().send(
            userId="me", 
            body=create_message
        ).execute()
        print(f" Email envoyé avec succès ! ID: {sent_message['id']}")
        return True
    except HttpError as error:
        print(f" Erreur lors de l'envoi : {error}")
        return False

def get_unread_messages(max_results: int = 20) -> list:
    """
    Récupère la liste des messages non lus du compte.
    
    Args:
        max_results: Nombre maximum de messages à récupérer
    
    Returns:
        Liste des messages non lus (from, subject, date, id)
    """
    service = get_gmail_service()
    
    try:
        results = service.users().messages().list(
            userId="me",
            q="is:unread",
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        unread_list = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me",
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = msg_data['payload']['headers']
            unread_list.append({
                'id': msg['id'],
                'from': next((h['value'] for h in headers if h['name'] == 'From'), ''),
                'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), ''),
                'date': next((h['value'] for h in headers if h['name'] == 'Date'), ''),
            })
        
        return unread_list
    except HttpError as error:
        print(f" Erreur lors de la lecture : {error}")
        return []

def mark_as_read(message_id: str) -> bool:
    """
    Marque un message comme lu.
    
    Args:
        message_id: ID du message à marquer comme lu
    
    Returns:
        True si succès, False sinon
    """
    service = get_gmail_service()
    
    try:
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f" Message {message_id} marqué comme lu")
        return True
    except HttpError as error:
        print(f" Erreur : {error}")
        return False