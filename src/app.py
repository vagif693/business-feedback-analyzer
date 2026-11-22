import sys, os, datetime, logging, uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from src.data_loader import load_data
from src.ollama_api import ask_ollama

load_dotenv()

PLACEHOLDER_KEYS = {"", "change-me", "supersecret"}


def load_secret_key():
    """Read the session-signing key from the environment and refuse to start without a real one."""
    key = os.environ.get("FLASK_SECRET_KEY", "")
    if key in PLACEHOLDER_KEYS or len(key) < 32:
        raise RuntimeError(
            "FLASK_SECRET_KEY is missing or too weak. Copy .env.example to .env and set a random key "
            "of at least 32 characters."
        )
    return key


def debug_enabled():
    """Debug mode is off unless FLASK_DEBUG=1 is set explicitly."""
    return os.environ.get("FLASK_DEBUG") == "1"


app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = load_secret_key()
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg'}

log = logging.getLogger(__name__)


def allowed_extension(filename):
    """Return the lower-case extension if it is allowed, otherwise None."""
    name = secure_filename(filename or '')
    if '.' not in name:
        return None
    ext = name.rsplit('.', 1)[1].lower()
    return ext if ext in ALLOWED_EXTENSIONS else None

def nice_time():
    return datetime.datetime.now().strftime("%H:%M")

def get_file_text(df):
    # Truncate to avoid super long texts for LLM prompt
    if "text_response" in df.columns:
        text = "\n".join(str(t) for t in df["text_response"])
        return text[:3000]
    return str(df.head())

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    chat_history = session.get("chat_history", [])
    uploaded = session.get("uploaded", False)
    error_msg = None
    upload_msg = None

    if request.method == "POST":
        # File upload
        if "upload_file" in request.form:
            newfile = request.files.get("datafile", None)
            ext = allowed_extension(newfile.filename) if newfile else None
            if newfile is None or not newfile.filename:
                error_msg = "Please choose a file to upload."
            elif ext is None:
                error_msg = "Unsupported file type. Please upload CSV, Excel, TXT, PDF, DOCX, or an image."
            else:
                upload_dir = app.config['UPLOAD_FOLDER']
                os.makedirs(upload_dir, exist_ok=True)
                fpath = os.path.join(upload_dir, f"{uuid.uuid4().hex}.{ext}")
                newfile.save(fpath)
                try:
                    df = load_data(fpath)
                    session["file_text"] = get_file_text(df)
                    session["uploaded"] = True
                    uploaded = True
                    chat_history = []
                    session["chat_history"] = chat_history
                    upload_msg = "File uploaded! You can now chat about your document."
                except Exception:
                    log.exception("Failed to load uploaded file")
                    error_msg = "Sorry, that file could not be read."
                    session["uploaded"] = False
                    uploaded = False
                finally:
                    os.remove(fpath)
        # Chat input
        elif "send_message" in request.form and session.get("uploaded"):
            msg = request.form.get("user_message","").strip()
            if msg:
                chat_history.append({"role":"user","msg":msg,"time":nice_time()})
                session["chat_history"] = chat_history
                prompt = f"Document data:\n{session.get('file_text','')}\nUser query: {msg}"
                try:
                    ai_resp = ask_ollama(prompt)
                except Exception as e:
                    ai_resp = f"AI Error: {e}"
                chat_history.append({"role":"ai","msg":ai_resp,"time":nice_time()})
                session["chat_history"] = chat_history
        session.modified = True

    return render_template("dashboard.html",
        chat_history=session.get("chat_history", []),
        uploaded=session.get("uploaded", False),
        error_msg=error_msg,
        upload_msg=upload_msg
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=debug_enabled())
