import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class NotificationSender:
    def __init__(self, config_path='config/notification_config.json'):
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)

    def send_team_notification(self, feedback_data):
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['team_email']
            msg['Subject'] = f"Customer Feedback Alert: {feedback_data['sentiment']} Sentiment"

            # Email body
            body = f"""
            Customer Feedback Notification:
            
            Customer Name: {feedback_data.get('customer_name', 'Unknown')}
            Order ID: {feedback_data.get('order_id', 'N/A')}
            Feedback Category: {feedback_data.get('feedback_category', 'General')}
            Sentiment: {feedback_data.get('sentiment', 'Neutral')}
            Sentiment Score: {feedback_data.get('sentiment_score', 50)}
            """
            
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.send_message(msg)
            
            logging.info("Team notification email sent successfully")
        
        except Exception as e:
            logging.error(f"Notification sending error: {e}")