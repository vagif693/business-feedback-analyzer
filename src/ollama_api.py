import requests
import json

def ask_ollama(prompt, model="gemma3:1b"):
    url = "http://localhost:11434/api/generate"
    response = requests.post(
        url,
        json={"model": model, "prompt": prompt},
        stream=True
    )
    response.raise_for_status()
    full_response = ''
    for line in response.iter_lines(decode_unicode=True):
        if not line.strip(): continue
        try:
            obj = json.loads(line)
            if "response" in obj:
                full_response += obj["response"]
        except Exception:
            pass
    return full_response.strip()