from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from pathlib import Path

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# Load environment variables: prefer .venv/.env (if present) then project .env
venv_env = Path('.venv/.env')
project_env = Path('.env')
if venv_env.exists():
    load_dotenv(venv_env)
elif project_env.exists():
    load_dotenv(project_env)
else:
    load_dotenv()

app = Flask(__name__)

# Read OpenAI key from environment; do not abort import if missing so the site can still serve static files
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# sanitize accidental quotes/whitespace: OPENAI_API_KEY= "sk-..." -> sk-...
if OPENAI_API_KEY:
    OPENAI_API_KEY = OPENAI_API_KEY.strip().strip('"').strip("'")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = None
if OpenAI is not None and OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        # keep client None but include the exception in logs if needed
        client = None

# Startup info (do not print the key itself)
if OPENAI_API_KEY:
    print("OPENAI_API_KEY appears to be set (loaded from .env or environment). OpenAI client will be initialized if package is available.")
else:
    print("OPENAI_API_KEY not found in environment or .env (server will return an error for chat calls).")


SYSTEM_PROMPT = (
    "You are Johann Sebastian Bach (1685–1750), the renowned German Baroque composer. "
    "Remain in character: scholarly, devout, patient, and methodical. Speak in a clear 18th-century tone, "
    "but make your explanations understandable for modern listeners."
)

MUSIC_GOD_PROMPT = (
    "You are Johann Sebastian Bach, elevated as the 'Music God' — an oracle of music: "
    "answer only music-related questions (theory, harmony, counterpoint, composition, instrumentation, history of music). "
    "If the user asks anything outside of music, politely refuse and steer them back to musical topics. "
    "Keep the 18th-century Bach persona, but prioritize concise, expert musical guidance."
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if client is None:
        return (
            jsonify(
                {
                    "error": "OpenAI client not configured. Set OPENAI_API_KEY in your environment or .env file and restart the server."
                }
            ),
            500,
        )

    music_god = bool(data.get("music_god"))
    chosen_system = MUSIC_GOD_PROMPT if music_god else SYSTEM_PROMPT

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": chosen_system},
                {"role": "user", "content": user_message},
            ],
        )
        text = response.choices[0].message.content
        return jsonify({"reply": text})
    except Exception as e:
        return jsonify({"error": f"API request failed: {e}"}), 500


if __name__ == "__main__":
    # Development server
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", 5000)), debug=True)
