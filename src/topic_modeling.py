# ML/NLP for topic extraction
def extract_topics(df):
    # Dummy topic extraction: find most common words
    topics = {}
    words = " ".join(df['cleaned'].values).split()
    for w in words:
        topics[w] = topics.get(w, 0) + 1
    sorted_topics = sorted(topics.items(), key=lambda item: item[1], reverse=True)
    return sorted_topics[:5]  # top 5 frequent words as 'topics'