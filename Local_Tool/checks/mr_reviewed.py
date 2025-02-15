import requests
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
API_BASE_URL = os.getenv("API_BASE_URL")
PROJECT_ID = os.getenv("PROJECT_ID")
AUTHOR = os.getenv("AUTHOR")

def count_all_time_reviewed_prs():
    """Zählt die Anzahl der überprüften PRs im Projekt."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    pr_url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls?state=all"
    response = requests.get(pr_url, headers=headers)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der PRs: {response.status_code}")
        return None

    prs = response.json()
    reviewed_pr_count = 0

    for pr in prs:
        pr_number = pr.get("number")
        review_url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls/{pr_number}/reviews"
        review_response = requests.get(review_url, headers=headers)

        if review_response.status_code != 200:
            print(f"Fehler beim Laden der Reviews für PR {pr_number}: {review_response.status_code}")
            continue

        reviews = review_response.json()
        if len(reviews) > 0:
            reviewed_pr_count += 1

    return reviewed_pr_count

def load_scored_prs():
    """Lädt die Anzahl der bewerteten PRs von der API."""
    url = f"{API_BASE_URL}/projects/get-project/{PROJECT_ID}"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        code_reviews_count = data.get("project", {}).get("code_reviews_count", 0)
        return code_reviews_count
    else:
        print(f"Fehler beim Laden der bewerteten PRs: {response.status_code}")
        return None

def update_score_for_reviews():
    """Aktualisiert die Punktzahl für die Anzahl der überprüften PRs im Projekt."""
    anz_reviewed_prs_in_project = count_all_time_reviewed_prs()
    anz_scored_prs_in_project = load_scored_prs()

    if anz_reviewed_prs_in_project is None or anz_scored_prs_in_project is None:
        return 0
    
    if anz_reviewed_prs_in_project > anz_scored_prs_in_project:
        difference = anz_reviewed_prs_in_project - anz_scored_prs_in_project
        return difference
    
    return 0
"""
        while difference > 0:
            # send_action("mr_reviewed")
"""

# print(load_scored_prs())