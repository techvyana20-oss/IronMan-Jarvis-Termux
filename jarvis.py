import os
import requests
import subprocess
import getpass

# ===============================
# CONFIG
# ===============================
API_FILE = os.path.expanduser("~/.jarvis_api_key")
MODEL = "gpt-3.5-turbo"

# ===============================
# TEXT TO SPEECH
# ===============================
def speak(text):
    try:
        subprocess.call(["espeak", text])
    except:
        print("[!] espeak not installed")

# ===============================
# SAVE API KEY SECURELY
# ===============================
def save_api_key(key):
    with open(API_FILE, "w") as f:
        f.write(key)
    os.chmod(API_FILE, 0o600)  # owner read/write only

# ===============================
# LOAD API KEY
# ===============================
def load_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            return f.read().strip()
    return None

# ===============================
# ASK USER FOR API KEY
# ===============================
def get_api_key():
    api_key = load_api_key()
    if api_key:
        return api_key

    print("🔐 Enter your OpenAI API key (hidden):")
    api_key = getpass.getpass("> ")
    save_api_key(api_key)
    print("✅ API key saved securely")
    return api_key

# ===============================
# CHATGPT REQUEST
# ===============================
def ask_jarvis(api_key, prompt):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Jarvis, a powerful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return "Error connecting to OpenAI API."

    return response.json()["choices"][0]["message"]["content"]

# ===============================
# MAIN LOOP
# ===============================
def main():
    api_key = get_api_key()

    print("\n🤖 JARVIS AI ACTIVATED")
    print("Type 'exit' to quit\n")
    speak("Jarvis activated. How can I help you?")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            speak("Goodbye sir.")
            print("👋 Exiting Jarvis")
            break

        reply = ask_jarvis(api_key, user_input)
        print("Jarvis:", reply)
        speak(reply)

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    main()
