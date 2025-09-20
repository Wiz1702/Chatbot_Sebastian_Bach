from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables: prefer .venv/.env (if present) then project .env
venv_env = Path(".venv/.env")
project_env = Path(".env")
if venv_env.exists():
    load_dotenv(venv_env)
elif project_env.exists():
    load_dotenv(project_env)
else:
    # still call load_dotenv() to allow default behavior (no-op if nothing)
    load_dotenv()


def get_openai_api_key_or_exit():
    """Return an OpenAI API key or exit with a clear message.

    Preference order:
      1. OPENAI_API_KEY environment variable
      2. Interactive prompt fallback for OPENAI_API_KEY
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    # If the key is wrapped with quotes or has accidental whitespace, sanitize it
    if openai_key:
        openai_key = openai_key.strip().strip('"').strip("'")

    if openai_key:
        return openai_key

    # Interactive fallback: ask the user for an OpenAI key
    try:
        key = input("OPENAI_API_KEY not set. Enter your OpenAI API key (or press Enter to exit): ").strip()
    except EOFError:
        key = None

    if not key:
        raise SystemExit(
            "OpenAI API key not provided. Set OPENAI_API_KEY in your environment or .env file, or run interactively to paste it."
        )

    return key


# Initialize OpenAI client with a validated OpenAI API key
client = OpenAI(api_key=get_openai_api_key_or_exit())

def bach_chat(user_input):
    system_prompt = """
You are Johann Sebastian Bach (1685–1750), the renowned German Baroque composer.
You must always remain in character: scholarly, devout, patient, and methodical.
Your speech should reflect the 18th-century tone of Bach, but be clear for modern listeners.
You are deeply knowledgeable in music theory, composition, counterpoint, and instruments.
Never break character.
"""

    response = client.chat.completions.create(
        model="gpt-5",  # or the latest available model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("🎼 Willkommen! Thou art now speaking with Johann Sebastian Bach.")
    while True:
        query = input("Thou: ")
        if query.lower() in ["quit", "exit"]:
            print("Bach: Farewell, and may thy music ever glorify God.")
            break
        answer = bach_chat(query)
        print("Bach:", answer)
