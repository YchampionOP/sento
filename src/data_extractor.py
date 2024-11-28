import logging
import re


class DataExtractor:
    def extract_details(self, email):
        try:
            # Extract customer name
            customer_name = self._extract_customer_name(email['sender'])
            
            # Extract order ID (if present)
            order_id = self._extract_order_id(email['content'])
            
            # Determine feedback category
            feedback_category = self._determine_feedback_category(email['subject'], email['content'])
            
            return {
                'customer_name': customer_name,
                'order_id': order_id,
                'feedback_category': feedback_category
            }
        
        except Exception as e:
            logging.error(f"Data extraction error: {e}")
            return {
                'customer_name': 'Unknown',
                'order_id': 'N/A',
                'feedback_category': 'General'
            }

    def _extract_customer_name(self, sender):
        # Extract name from email address or sender string
        match = re.search(r'^([^<]+)', sender)
        return match.group(1).strip() if match else 'Customer'

    def _extract_order_id(self, content):
        # Look for common order ID patterns
        match = re.search(r'(Order|Ref)[\s:]*(\w{6,10})', content, re.IGNORECASE)
        return match.group(2) if match else 'N/A'

    def _determine_feedback_category(self, subject, content):
        keywords = {
            'product': ['product', 'item', 'quality'],
            'service': ['service', 'support', 'help'],
            'delivery': ['delivery', 'shipping', 'arrived']
        }
        
        text = (subject + ' ' + content).lower()
        
        for category, terms in keywords.items():
            if any(term in text for term in terms):
                return category
        
        return 'General'