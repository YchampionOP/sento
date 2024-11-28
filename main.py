import logging
from src.email_retriever import EmailRetriever
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_extractor import DataExtractor
from src.google_form_handler import GoogleFormHandler
from src.notification_sender import NotificationSender
from src.trubot_integration import TrubotAutomation

class CustomerFeedbackAutomationSuite:
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='logs/automation_errors.log'
        )
        
        # Initialize components
        self.email_retriever = EmailRetriever()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.data_extractor = DataExtractor()
        self.google_form_handler = GoogleFormHandler()
        self.notification_sender = NotificationSender()
        self.trubot_automation = TrubotAutomation()

    def run_automation(self):
        try:
            # Retrieve emails
            emails = self.email_retriever.fetch_emails()
            logging.info(f"Retrieved {len(emails)} emails")

            for email in emails:
                # Analyze sentiment
                sentiment = self.sentiment_analyzer.analyze(email['content'])
                
                # Extract data
                extracted_data = self.data_extractor.extract_details(email)
                
                # Add sentiment to extracted data
                extracted_data['sentiment'] = sentiment['type']
                extracted_data['sentiment_score'] = sentiment['score']

                # Submit to Google Form
                self.google_form_handler.submit(extracted_data)
                
                # Send notification
                self.notification_sender.send_team_notification(extracted_data)
                
                # Optional: Use TruBot for further automation if needed
                self.trubot_automation.process_feedback(extracted_data)

            logging.info("Automation workflow completed successfully")

        except Exception as e:
            logging.error(f"Automation failed: {str(e)}")

def main():
    automation_suite = CustomerFeedbackAutomationSuite()
    automation_suite.run_automation()

if __name__ == "__main__":
    main()