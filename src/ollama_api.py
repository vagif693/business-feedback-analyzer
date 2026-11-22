import json
import logging

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 120

log = logging.getLogger(__name__)


def ask_ollama(prompt, model="gemma3:1b"):
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt},
        stream=True,
        timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
    )
    response.raise_for_status()
    full_response = ''
    for line in response.iter_lines(decode_unicode=True):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            log.warning("Skipping malformed line from Ollama")
            continue
        if "response" in obj:
            full_response += obj["response"]
    return full_response.strip()
