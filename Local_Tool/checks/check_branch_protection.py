import requests
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# GitHub-Token und Repository-Name aus Umgebungsvariablen abrufen
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def check_branch_protection():
    """Überprüft, ob der Haupt- oder Master-Branch im GitHub-Repository geschützt ist."""
    possible_branches = ["master", "main"]
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    branch_found = False

    for branch_name in possible_branches:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/branches/{branch_name}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            real_branch_name = data.get("name")

            if real_branch_name != branch_name:
                continue
            branch_found = True

            if data.get("protected", False):
                return True
            else:
                return False

        elif response.status_code == 404:
            continue
        else:
            return None
        
    return None
