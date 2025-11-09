# Sentiment scoring/classification
from textblob import TextBlob

def analyze_sentiment(df):
    # Dummy sentiment analysis using textblob
    def get_sentiment(text):
        score = TextBlob(text).sentiment.polarity
        if score > 0.2:
            return "positive"
        elif score < -0.2:
            return "negative"
        else:
            return "neutral"
    df['sentiment'] = df['cleaned'].apply(get_sentiment)
    return df