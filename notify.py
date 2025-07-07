import requests

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
# ---------------------

# --- TELEGRAM NOTIFICATION FUNCTIONS ---
def send(text):
    """Sends a message to Telegram and returns the message_id."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['result']['message_id']
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return None

def edit(message_id, text):
    """Edits an existing Telegram message."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error editing Telegram message: {e}")

def delete(message_id):
    """Deletes a Telegram message."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "message_id": message_id}
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException:
        # Ignore if message doesn't exist
        pass
    
def file(path, caption=""):
    """Sends a file to Telegram with an optional caption."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(path, 'rb') as doc_file:
        files = {'document': doc_file}
        payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
        try:
            # Increased timeout for potentially large log files
            requests.post(url, files=files, data=payload, timeout=600)
        except requests.exceptions.RequestException as e:
            print(f"Error sending file to Telegram: {e}")
# --- END OF TELEGRAM NOTIFICATION FUNCTIONS ---