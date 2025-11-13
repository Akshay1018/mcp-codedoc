from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime

#===============================================
# Notes MCP Server
#===============================================

mcp = FastMCP("Notes")

BASE_DIR = os.path.dirname(__file__)
NOTES_DIR = os.path.join(BASE_DIR, "documentation_notes")
MANUAL_NOTES_FILE = os.path.join(BASE_DIR, "notes.txt")

# Ensure folders exist
os.makedirs(NOTES_DIR, exist_ok=True)

#-----------------------------------------------
# Utility Functions
#-----------------------------------------------
def ensure_manual_notes_exists():
    if not os.path.exists(MANUAL_NOTES_FILE):
        with open(MANUAL_NOTES_FILE, "w") as f:
            f.write("")

def get_latest_notes_file():
    """Return the latest auto-generated notes file path"""
    files = [f for f in os.listdir(NOTES_DIR) if f.startswith("notes_") and f.endswith(".txt")]
    if not files:
        return None
    # Sort by timestamp in filename
    files.sort(reverse=True)
    return os.path.join(NOTES_DIR, files[0])

#-----------------------------------------------
# Core MCP Tools
#-----------------------------------------------
@mcp.tool()
def add_note(note: str) -> str:
    """
    Add a note manually to the global notes file.
    """
    ensure_manual_notes_exists()
    with open(MANUAL_NOTES_FILE, "a") as f:
        f.write(note + "\n")
    return f"📝 Note saved: {note}"

@mcp.tool()
def read_notes(source: str = "latest") -> str:
    """
    Read notes from either:
      - 'latest' (auto-generated notes)
      - 'manual' (your manual notes.txt)
    """
    if source == "latest":
        latest_file = get_latest_notes_file()
        if not latest_file:
            return "⚠️ No auto-generated documentation notes found."
        with open(latest_file, "r") as f:
            return f"📄 Latest Notes from {os.path.basename(latest_file)}:\n\n" + f.read().strip()
    else:
        ensure_manual_notes_exists()
        with open(MANUAL_NOTES_FILE, "r") as f:
            content = f.read().strip()
        return content or "🗒️ No manual notes found."

@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Return the most recent line from the latest notes file.
    """
    latest_file = get_latest_notes_file()
    if not latest_file:
        return "⚠️ No notes found."
    with open(latest_file, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes found."

@mcp.prompt()
def summarise_notes() -> str:
    """
    Summarise the latest notes file.
    """
    latest_file = get_latest_notes_file()
    if not latest_file:
        return "⚠️ No notes to summarise."
    with open(latest_file, "r") as f:
        content = f.read().strip()
    if not content:
        return "⚠️ Notes file is empty."
    return f"🧠 Summary of the latest notes ({os.path.basename(latest_file)}):\n\n{content}"
