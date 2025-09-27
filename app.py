from flask import Flask, render_template, request, jsonify
import uuid
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

# Simple in-memory rolling memory for chat sessions: { session_id: [ {role, content}, ... ] }
SESSION_MEMORY = {}
MAX_MEMORY_MESSAGES = 8  # keep N most recent role/content pairs per session

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
    # optional session id; if not provided, create one and return it
    session_id = data.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
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
        # build message list including rolling memory for the session
        memory = SESSION_MEMORY.get(session_id, [])
        messages = [{"role": "system", "content": chosen_system}] + memory + [{"role": "user", "content": user_message}]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        text = response.choices[0].message.content

        # update session memory: append user + assistant messages and trim
        entry_user = {"role": "user", "content": user_message}
        entry_assistant = {"role": "assistant", "content": text}
        new_memory = (memory + [entry_user, entry_assistant])[-MAX_MEMORY_MESSAGES:]
        SESSION_MEMORY[session_id] = new_memory

        return jsonify({"reply": text, "session_id": session_id})
    except Exception as e:
        return jsonify({"error": f"API request failed: {e}"}), 500


if __name__ == "__main__":
    # Development server
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", 5000)), debug=True)


@app.route("/chat_test", methods=["POST"])
def chat_test():
    """Simulated chat endpoint for local testing without calling the OpenAI API.
    It obeys session_id and music_god flags and updates SESSION_MEMORY like the real endpoint.
    """
    data = request.get_json() or {}
    session_id = data.get("session_id") or str(uuid.uuid4())
    user_message = data.get("message", "")
    music_god = bool(data.get("music_god"))

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Simulate assistant behavior
    if music_god and not ("music" in user_message.lower() or "counterpoint" in user_message.lower() or "harmony" in user_message.lower()):
        reply = "I will speak only of music. Pray, ask me about counterpoint, harmony, or a composition."
    else:
        reply = f"[Simulated Bach reply to: {user_message}]"

    # Update rolling memory as the real endpoint does
    memory = SESSION_MEMORY.get(session_id, [])
    entry_user = {"role": "user", "content": user_message}
    entry_assistant = {"role": "assistant", "content": reply}
    new_memory = (memory + [entry_user, entry_assistant])[-MAX_MEMORY_MESSAGES:]
    SESSION_MEMORY[session_id] = new_memory

    return jsonify({"reply": reply, "session_id": session_id})
