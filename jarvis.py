import os
import requests
import subprocess
import getpass
import datetime
import socket
import json

# ===============================
# CONFIG
# ===============================
API_FILE = os.path.expanduser("~/.jarvis_api_key")
MODEL = "gpt-3.5-turbo"
API_URL = "https://api.openai.com/v1/chat/completions"

# ===============================
# SPEAK
# ===============================
def speak(text):
    try:
        subprocess.run(["espeak", text], stdout=subprocess.DEVNULL)
    except:
        pass

# ===============================
# INTERNET CHECK
# ===============================
def internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except:
        return False

# ===============================
# API KEY HANDLING
# ===============================
def load_api_key():
    if os.path.exists(API_FILE):
        return open(API_FILE).read().strip()
    return None

def save_api_key(key):
    with open(API_FILE, "w") as f:
        f.write(key)
    os.chmod(API_FILE, 0o600)

def get_api_key():
    key = load_api_key()
    if key:
        return key

    print("🔐 Enter OpenAI API Key (hidden):")
    key = getpass.getpass("> ").strip()

    if not key.startswith("sk-"):
        print("❌ Invalid API key format")
        exit()

    save_api_key(key)
    print("✅ API key saved securely")
    return key

# ===============================
# CHATGPT REQUEST (FIXED)
# ===============================
def ask_ai(api_key, prompt):
    if not internet_available():
        return "No internet connection."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Jarvis, an intelligent AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=40
        )

        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text}"

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# ===============================
# OFFLINE COMMANDS
# ===============================
def offline_commands(text):
    text = text.lower()

    if "time" in text:
        return datetime.datetime.now().strftime("🕒 %H:%M:%S")

    if "date" in text:
        return datetime.datetime.now().strftime("📅 %d %B %Y")

    if "system info" in text:
        return subprocess.getoutput("uname -a")

    if text.startswith("run "):
        cmd = text.replace("run ", "")
        return subprocess.getoutput(cmd)

    return None

# ===============================
# MAIN
# ===============================
def main():
    api_key = get_api_key()

    print("\n🤖 JARVIS AI ACTIVATED")
    print("Type 'exit' to quit\n")

    speak("Jarvis activated. Ready to assist.")

    while True:
        user = input("You: ").strip()

        if user.lower() in ["exit", "quit"]:
            speak("Goodbye sir.")
            print("👋 Exiting Jarvis")
            break

        offline = offline_commands(user)
        if offline:
            print("Jarvis:", offline)
            speak(offline)
            continue

        reply = ask_ai(api_key, user)
        print("Jarvis:", reply)
        speak(reply)

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    main()
