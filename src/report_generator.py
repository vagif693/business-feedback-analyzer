# Compiles visuals, metrics, NL summaries
import matplotlib.pyplot as plt
import os
from src.ollama_api import ask_ollama

def generate_report(df, topics, sentiments):
    words, counts = zip(*topics)
    chart_path = os.path.join('static', 'topics.png')
    plt.figure()
    plt.bar(words, counts)
    plt.title('Top Topics')
    plt.savefig(chart_path)
    plt.close()

    pos = (df['sentiment'] == 'positive').sum()
    neg = (df['sentiment'] == 'negative').sum()
    neu = (df['sentiment'] == 'neutral').sum()
    basic_summary = f"Feedback contains {pos} positive, {neg} negative, and {neu} neutral responses. Top topics: {', '.join(words)}"
    # Request LLM-enhanced summary
    llm_prompt = f"Summarize this business feedback for an executive meeting: {basic_summary}"
    llm_summary = ask_ollama(llm_prompt)
    return llm_summary, [chart_path]