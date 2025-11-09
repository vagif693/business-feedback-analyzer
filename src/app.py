import sys, os, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, session
from src.data_loader import load_data
from src.ollama_api import ask_ollama

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = 'supersecret'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../data')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            if newfile and newfile.filename:
                fpath = os.path.join(app.config['UPLOAD_FOLDER'], newfile.filename)
                newfile.save(fpath)
                try:
                    df = load_data(fpath)
                    session["file_text"] = get_file_text(df)
                    session["uploaded"] = True
                    uploaded = True
                    chat_history = []
                    session["chat_history"] = chat_history
                    upload_msg = "File uploaded! You can now chat about your document."
                except Exception as e:
                    error_msg = f"Error loading file: {e}"
                    session["uploaded"] = False
                    uploaded = False
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
    app.run(debug=True)