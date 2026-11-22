# Business Survey/Feedback Analyzer

[![CI](https://github.com/vagif693/business-feedback-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/vagif693/business-feedback-analyzer/actions/workflows/ci.yml)

Upload customer feedback (CSV, Excel, TXT, PDF, DOCX or an image) and chat with a local LLM (Ollama) about it in a web dashboard.

## Security audit (November 2026)

I audited this project, which I wrote in November 2025, with Bandit, Semgrep and a manual code review, then fixed every finding on the `security-audit` branch. Each fix has a test that fails if the bug comes back.

| # | Finding | Severity | Found by | Fix |
|---|---------|----------|----------|-----|
| 1 | Path traversal: the uploaded filename was used as the save path, so `../../src/app.py` could overwrite code | Critical | Manual review | [09c9292](https://github.com/vagif693/business-feedback-analyzer/commit/09c9292) |
| 2 | Stored XSS: `\|safe` disabled escaping of chat messages and LLM output | High | Semgrep, manual review | [7c59d6a](https://github.com/vagif693/business-feedback-analyzer/commit/7c59d6a) |
| 3 | `debug=True` exposed the Werkzeug debugger (remote code execution) | High | Bandit, Semgrep | [57942af](https://github.com/vagif693/business-feedback-analyzer/commit/57942af) |
| 4 | Hard-coded `secret_key`, so session cookies could be forged | High | Bandit (rated Low) | [57942af](https://github.com/vagif693/business-feedback-analyzer/commit/57942af) |
| 5 | `.env` and bytecode committed to the repository | Medium | Manual review | [e8f1249](https://github.com/vagif693/business-feedback-analyzer/commit/e8f1249) |
| 6 | No upload size or file-type limits (denial of service through OCR) | Medium | Manual review | [09c9292](https://github.com/vagif693/business-feedback-analyzer/commit/09c9292) |
| 7 | No CSRF protection on forms | Medium | Manual review | [6da97f8](https://github.com/vagif693/business-feedback-analyzer/commit/6da97f8) |
| 8 | Raw exceptions shown to users; no timeout on LLM requests | Low | Bandit, manual review | [6da97f8](https://github.com/vagif693/business-feedback-analyzer/commit/6da97f8), [d5eb089](https://github.com/vagif693/business-feedback-analyzer/commit/d5eb089) |
| 9 | Container ran as root and `COPY . .` put `.env` into the image | Medium | Manual review | [fb47cd3](https://github.com/vagif693/business-feedback-analyzer/commit/fb47cd3), [6b66930](https://github.com/vagif693/business-feedback-analyzer/commit/6b66930) |

**Main lesson:** the scanners flagged 4 of the 9 issues. The only critical one, path traversal, was found by reading the code. Scanners are a safety net, not a replacement for review.

### Known limitations

- **Prompt injection:** a document can still try to steer the model's answers. Output is escaped, so it cannot run code in the browser, but answers should not be treated as trusted.
- **No authentication:** the app is meant to run locally for one user. The compose file binds it to `127.0.0.1` only.
- **Session storage:** extracted document text is kept in a signed, not encrypted, session cookie, so it is visible to the user who uploaded it.
- **Git history:** the old `.env` remains in history. It only held placeholder values; real secrets would have to be rotated.

## Run it

You need Python 3.13 and [Ollama](https://ollama.com) with the `gemma3:1b` model.

```bash
git clone https://github.com/vagif693/business-feedback-analyzer.git
cd business-feedback-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put a random key in `.env` (`python3 -c "import secrets; print(secrets.token_hex(32))"`), then start the app:

```bash
python src/app.py
```

Open http://127.0.0.1:5000. The app refuses to start without a strong `FLASK_SECRET_KEY`.

### With Docker

```bash
docker compose up --build
```

Open http://127.0.0.1:8000. The container runs as a non-root user with a read-only filesystem, no Linux capabilities, and a port bound to localhost only.

## Tests and CI

```bash
pip install pytest
python -m pytest -v
```

24 tests cover path traversal, upload limits, XSS escaping, CSRF, secret-key and debug configuration, and LLM request timeouts. GitHub Actions runs the tests, Bandit, Semgrep, pip-audit, and a Docker smoke test on every push and pull request.

## Project structure

```
src/
  app.py            Flask app: upload, chat, security configuration
  data_loader.py    Reads CSV, Excel, TXT, PDF, DOCX and images (OCR)
  ollama_api.py     Client for the local Ollama API, with timeouts
  preprocessing.py, sentiment_analysis.py, topic_modeling.py, report_generator.py
                    Early analysis modules, not yet wired into the dashboard
templates/
  dashboard.html    Web dashboard
tests/              pytest suite
Dockerfile          Hardened image (non-root, gunicorn, health check)
docker-compose.yml  Locked-down local deployment
```
