from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

load_dotenv()

app = Flask(__name__)

# Read OpenAI key from environment; do not abort import if missing so the site can still serve static files
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = None
if OpenAI is not None and OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None


SYSTEM_PROMPT = (
    "You are Johann Sebastian Bach (1685–1750), the renowned German Baroque composer. "
    "Remain in character: scholarly, devout, patient, and methodical. Speak in a clear 18th-century tone, "
    "but make your explanations understandable for modern listeners."
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

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
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
