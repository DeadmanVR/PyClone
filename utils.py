# --- STATE MANAGEMENT FUNCTIONS ---
def save(message_id, message_id_file):
    """Saves the message ID to a file."""
    with open(message_id_file, 'w') as f:
        f.write(str(message_id))

def load(message_id_file):
    """Loads the last message ID from a file."""
    try:
        with open(message_id_file, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None
# --- END OF STATE MANAGEMENT FUNCTIONS ---

# --- HELPER FOR UI ---
def formats(job_statuses, status_text="Initiated"):
    """Formats the multi-line status message for Telegram."""
    header = f"*Backup Process {status_text}*\n" + "-" * 25
    lines = [f"`{name:<12}` {status}" for name, status in job_statuses.items()]
    footer = "-" * 25
    return f"{header}\n" + "\n".join(lines) + f"\n{footer}"

def progress(percentage, length=10):
    """Creates a text-based progress bar."""
    filled_length = int(length * percentage // 100)
    bar = '█' * filled_length + '─' * (length - filled_length)
    return f"[{bar}] {percentage}%"
# --- END OF HELPER FOR UI ---