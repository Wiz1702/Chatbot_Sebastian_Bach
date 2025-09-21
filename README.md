# Bach Chatbot

This is a simple chatbot that speaks in the voice of Johann Sebastian Bach (1685–1750).  
It uses the OpenAI API to generate responses, always staying in character as the Baroque composer.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/bach-chatbot.git
   cd bach-chatbot

 A small Flask web app that lets you "talk" with Johann Sebastian Bach. The application uses the OpenAI Python client to generate responses and supports a focused "Music God" mode and a Dark Mode UI.

 This README explains how to set up and run the project locally.

 ## Requirements
 - Python 3.8+ (3.11 recommended)
 - git

 ## Quick start

 1. Create and activate a virtual environment (recommended):

 ```bash
 python3 -m venv .venv
 source .venv/bin/activate
 ```

 2. Install dependencies:

 ```bash
 pip install -r requirements.txt
 ```

 3. Create a `.env` file (or put the key in `.venv/.env`) with your OpenAI API key and optional model name. Do NOT commit this file.

 ```
 OPENAI_API_KEY=sk-REPLACE_ME
 # optional
 MODEL_NAME=gpt-4o-mini
 ```

 4. Start the Flask development server:

 ```bash
 python app.py
 # or (without activating the venv)
 .venv/bin/python app.py
 ```

 5. Open your browser at http://127.0.0.1:5000

 ## UI features
 - Dark Mode: Toggle in the left panel — the app will persist your preference.
 - Music God: Toggle the specialized mode where "Bach" will answer only music-related questions.

 ## Security notes
 - Never commit `.env` or any file containing your API keys. `.gitignore` in this repo already excludes `.env` and `.venv/.env`.
 - If you believe a key was exposed, revoke it immediately at https://platform.openai.com/account/api-keys and create a new one.

 ## Development notes
 - The app uses the OpenAI Python client and calls `client.chat.completions.create(...)`. Ensure the `MODEL_NAME` you set is available for your account.
 - The Flask server runs in debug mode by default in `app.py`. For production, run behind a WSGI server (Gunicorn / uWSGI) and set proper environment variables.

 ## Troubleshooting
 - `zsh: command not found: python` — run the script with the venv python: `.venv/bin/python app.py` or install Python 3.
 - If the UI shows errors about OpenAI client not configured, ensure `OPENAI_API_KEY` is present in `.env` (or exported in the shell) and restart the server.

 