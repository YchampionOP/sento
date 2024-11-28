import logging

from textblob import TextBlob


class SentimentAnalyzer:
    def analyze(self, text):
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Categorize sentiment
            if polarity > 0.2:
                sentiment_type = 'Positive'
            elif polarity < -0.2:
                sentiment_type = 'Negative'
            else:
                sentiment_type = 'Neutral'
            
            # Normalize sentiment score to 0-100 scale
            sentiment_score = round((polarity + 1) * 50, 2)
            
            return {
                'type': sentiment_type,
                'score': sentiment_score
            }
        
        except Exception as e:
            logging.error(f"Sentiment analysis error: {e}")
            return {
                'type': 'Neutral',
                'score': 50.0
            }