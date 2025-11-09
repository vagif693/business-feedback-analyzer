# Business Survey/Feedback Analyzer

Automatically analyze feedback or survey data using ML, NLP, and LLMs. Extract topics, detect sentiment, find actionable patterns, and generate business-friendly visual and textual reports — all on a web dashboard.

## Features

- Upload CSV/Excel feedback data via the dashboard
- Automatic data cleaning, topic modeling, and sentiment analysis
- Insights, trends, and critical issues detection
- Visual charts and wordclouds for easy understanding
- Natural-language summary reports using Ollama LLM
- Results downloadable, and expand to real business data

## Usage

1. Clone repo and install requirements:
    ```bash
    git clone https://github.com/your-user/business-feedback-analyzer.git
    cd business-feedback-analyzer
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Start the web app:
    ```bash
    export FLASK_APP=src.app
    flask run
    ```
   Or, using Docker:
    ```bash
    docker build -t feedback-analyzer .
    docker run -p 5000:5000 feedback-analyzer
    ```

3. Open your browser: [http://localhost:5000](http://localhost:5000)

4. Upload your survey/feedback CSV file via the interface!

## Project Structure

See the source files and comments for each module’s role.

## Requirements

See `requirements.txt`.

## Next Steps

- Add your company's survey data in `/data`
- Explore `notebooks/` for custom analysis
- Expand frontend as needed
