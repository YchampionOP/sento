import json
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleFormHandler:
    def __init__(self, config_path='config/sheets_config.json'):
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        
        # Setup Google Sheets service
        self.sheets_service = self._setup_sheets_service()

    def _setup_sheets_service(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_authorized_user_file(
            'config/sheets_credentials.json', SCOPES)
        return build('sheets', 'v4', credentials=creds)

    def submit(self, feedback_data):
        try:
            spreadsheet_id = self.config['spreadsheet_id']
            
            # Prepare row data
            row_data = [
                feedback_data['customer_name'],
                feedback_data.get('order_id', 'N/A'),
                feedback_data['feedback_category'],
                feedback_data['sentiment'],
                feedback_data['sentiment_score']
            ]
            
            # Append to sheet
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A:E',
                valueInputOption='RAW',
                body={'values': [row_data]}
            ).execute()
            
            logging.info(f"Submitted feedback to Google Sheets: {result}")
        
        except Exception as e:
            logging.error(f"Google Form submission error: {e}")