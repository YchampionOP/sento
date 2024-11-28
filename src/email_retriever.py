import base64
import json
import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class EmailRetriever:
    def __init__(self, config_path='config/gmail_config.json'):
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        
        # Setup Gmail service
        self.gmail_service = self._setup_gmail_service()

    def _setup_gmail_service(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        
        # Token management
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/gmail_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)

    def fetch_emails(self, query='is:unread'):
        try:
            # Fetch unread emails
            results = self.gmail_service.users().messages().list(
                userId='me', q=query).execute()
            messages = results.get('messages', [])
            
            processed_emails = []
            
            for msg in messages:
                email_data = self._process_email(msg['id'])
                if email_data:
                    processed_emails.append(email_data)
            
            return processed_emails
        
        except Exception as e:
            logging.error(f"Email retrieval error: {e}")
            return []

    def _process_email(self, msg_id):
        try:
            msg = self.gmail_service.users().messages().get(
                userId='me', id=msg_id, format='full').execute()
            
            # Extract headers
            headers = msg['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            
            # Extract body
            parts = msg['payload'].get('parts', [])
            if parts:
                body = parts[0]['body'].get('data', '')
            else:
                body = msg['payload']['body'].get('data', '')
            
            # Decode body
            body = base64.urlsafe_b64decode(body).decode('utf-8')
            
            return {
                'id': msg_id,
                'sender': sender,
                'subject': subject,
                'content': body
            }
        
        except Exception as e:
            logging.error(f"Error processing individual email: {e}")
            return None