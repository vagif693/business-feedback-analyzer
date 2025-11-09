# Cleaning, normalization, feature extraction
import re

def preprocess_text(df):
    df['cleaned'] = df['text_response'].astype(str).str.lower().apply(lambda t: re.sub(r'[^a-zA-Z0-9\s]', '', t))
    return df