import json
import logging

import requests


class TrubotAutomation:
    def __init__(self, config_path='config/trubot_config.json'):
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        
        # Setup authentication
        self.headers = {
            'Authorization': f"Bearer {self.config['api_token']}",
            'Content-Type': 'application/json'
        }

    def process_feedback(self, feedback_data):
        try:
            # Send feedback data to TruBot for further processing
            response = requests.post(
                self.config['automation_endpoint'],
                headers=self.headers,
                json=feedback_data
            )
            
            # Check response
            if response.status_code == 200:
                logging.info("Feedback processed by TruBot successfully")
            else:
                logging.warning(f"TruBot processing failed: {response.text}")
        
        except Exception as e:
            logging.error(f"TruBot integration error: {e}")