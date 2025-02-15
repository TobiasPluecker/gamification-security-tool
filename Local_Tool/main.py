import sys
import os
import subprocess
from colorama import init, Fore, Style
from dotenv import load_dotenv
import requests

from Local_Tool.checks.mr_reviewed import update_score_for_reviews

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
AUTHOR = os.getenv("AUTHOR", "default_author")
PROJECT_ID = os.getenv("PROJECT_ID")


print(f"API_BASE_URL: Project_ID: {API_BASE_URL} {PROJECT_ID}")

init()
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Checks
from Local_Tool.checks.binary_check import check_binary_files
from Local_Tool.checks.secrets_check import check_credentials

# Possible problems that can be found
from Local_Tool.checks.check_branch_protection import check_branch_protection
from Local_Tool.checks.check_license import check_for_license
from Local_Tool.checks.check_webhooks import scan_project_for_insecure_webhooks
from Local_Tool.checks.check_api_endpoints import check_api_security

# Mapping of check types to action strings
check_action_map = {
    'binary': 'binary_file_committed',
    'credentials': 'credentials_committed',
}

def get_staged_files():
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: {e.stderr.decode()}{Style.RESET_ALL}")
        sys.exit(1)
    
def get_all_files(root):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            all_files.append(filepath)
    return all_files

def print_check_result(check_name, success, message=None):
    if success:
        print(f"{Fore.GREEN}✓ {check_name} successful{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ {check_name} failed{Style.RESET_ALL}")
        if message:
            print(f"  {message}")

def run_checks(files):
    """
    Executes all checks and collects identified errors in a list.
    Each error dictionary contains at least:
      - 'check': (binary | credentials)
      - 'message': A string with the error description
    """
    errors = []
    print("\nRunning security checks...")

    # Check for binary files
    binary_error = check_binary_files(files)
    print_check_result("Binary File Check", not binary_error, binary_error['message'] if binary_error else None)
    if binary_error:
        binary_error['check'] = 'binary'
        errors.append(binary_error)

    # Check for secrets
    try:
        secret_errors = check_credentials(files)
        if not secret_errors:
            print_check_result("Credentials Check", True)
        else:
            for error in secret_errors:
                print_check_result(
                    "Credentials Check", 
                    False, 
                    f"In file {error['file']} (line {error.get('line', 'unknown')}): {error['message']}"
                )
                error['check'] = 'credentials'
                errors.append(error)
    except Exception as e:
        print_check_result("Credentials Check", False, f"Error during check: {str(e)}")
        errors.append({
            'check': 'credentials',
            'message': f"Error during check execution: {str(e)}"
        })

    return errors

def send_action(action):
    """
    Sends an action to the API.
    """
    url = f"{API_BASE_URL}/api/action-report"
    payload = {
        "project_id": PROJECT_ID,
        "action": action,
        "author": AUTHOR
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"{Fore.RED}API error: {response.status_code} - {response.text}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}API Response: {response.json()}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Network error sending to API: {str(e)}{Style.RESET_ALL}")

def load_current_problems():
    current_problems = []
    url = f"{API_BASE_URL}/projects/get-project/{PROJECT_ID}"
    headers = {"Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)
    print(f"API Response: {response.status_code}")
    
    data = response.json()
    security_challenges = data.get("project", {}).get("security_challenges", [])

    if not security_challenges:
        return current_problems

    for challenge in security_challenges:
        current_problems.append(challenge.get("problem", "Unknown Problem"))
    
    print(current_problems)
    
    return current_problems

def challenge_solved(challenge: str):
    url = f"{API_BASE_URL}/api/finish-challenge"
    payload = {
        "project_id": PROJECT_ID,
        "challenge": challenge,
        "author": AUTHOR
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"{Fore.RED}API error: {response.status_code} - {response.text}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}API Response: {response.json()}{Style.RESET_ALL}")
    except requests.RequestException as e:  
        print(f"{Fore.RED}Network error sending to API: {str(e)}{Style.RESET_ALL}")

def report_problem(problem: str):
    url = f"{API_BASE_URL}/api/problem-report"
    payload = {"project_id": PROJECT_ID, "problem": problem}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"{Fore.RED}API error: {response.status_code} - {response.text}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}API Response: {response.json()}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Network error sending to API: {str(e)}{Style.RESET_ALL}")

def find_problems(files):
    """
    Tries to find problems that exist in the project but should not block the commit.
    """
    problems = load_current_problems()
    current_problems = []

    if check_branch_protection() is False:
        current_problems.append("No Branch Protection")

    if check_for_license() is False:
        current_problems.append("Add a license")

    if scan_project_for_insecure_webhooks(find_git_root()) is False:
        print("Insecure Webhook found")
        current_problems.append("Insecure Webhook")

    if check_api_security(find_git_root()) is False:
        print("Insecure API Endpoint found")
        current_problems.append("Insecure API Endpoint")

    # Report solved problems to the API
    for challenge in problems:
        if challenge not in current_problems:
            challenge_solved(challenge)

    # Report new problems to the API
    for challenge in current_problems:
        if challenge not in problems:
            report_problem(challenge)

def find_git_root(path: str = os.getcwd()) -> str:
    """
    Walks up from the given path until a directory containing a '.git' folder is found.
    If no such directory is found, returns the original path.
    """
    current_path = path
    while current_path != os.path.dirname(current_path):  # Stop at the filesystem root
        if os.path.isdir(os.path.join(current_path, '.git')):
            return current_path
        current_path = os.path.dirname(current_path)
    return path

def main():
    # Redirect stdout to stderr to avoid conflicts with the pre-commit hook.
    sys.stdout = sys.stderr

    print(f"{Fore.CYAN}🔍 Starting Pre-Commit Checks{Style.RESET_ALL}")

    anz = update_score_for_reviews()
    while anz > 0:
        send_action("mr_reviewed")

    files = get_staged_files()
    find_problems(files)

    print(f"Checking {len(files)} files...")

    errors = run_checks(files)
    if not errors:
        print("\nNo errors found. Sending 'no_mistake' to the API...")
        send_action("no_mistake")
    else:
        print("\nMistakes found. Sending actions to the API...")
        for error in errors:
            check_type = error.get('check')
            if check_type in check_action_map:
                action_str = check_action_map[check_type]
                send_action(action_str)
            else:
                print(f"{Fore.YELLOW}Unknown check type: {check_type}{Style.RESET_ALL}")

    print("\nConclusion:")
    if errors:
        print(f"{Fore.RED}❌ {len(errors)} errors found{Style.RESET_ALL}")
        sys.exit(1)
    else:
        print(f"{Fore.GREEN}✅ All checks passed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
