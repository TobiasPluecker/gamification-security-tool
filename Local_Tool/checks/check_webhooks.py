import os
import yaml
import re
import pathspec

def load_config():
    """
    Loads the configuration file.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def check_webhooks(files):
    """
    Checks the provided files for potentially insecure webhook calls.
    
    It searches for lines containing 'webhook', 'requests.post' or 'requests.get'.
    Found URL strings are then checked to ensure that HTTPS is used and, if specified in the
    configuration, that the domain is included in the list of safe domains.
    """
    issues = []
    config = load_config()
    
    # Retrieve safe domains from the configuration (if defined)
    safe_domains = config.get("webhook_safe_domains", [])
    
    # Regex to find URL strings (e.g. "http://..." or "https://...")
    url_pattern = re.compile(r"(https?://[^\s'\"]+)")
    
    for file in files:
        if not os.path.isfile(file):
            continue

        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    # Look for hints of webhook calls
                    if "webhook" in line.lower() or "requests.post" in line or "requests.get" in line:
                        matches = url_pattern.findall(line)
                        for url in matches:
                            # Check if HTTPS is used
                            if not url.startswith("https://"):
                                issues.append({
                                    'file': file,
                                    'line': line_num,
                                    'message': f"Insecure webhook (not using HTTPS): {url}",
                                })
                            
                            # Extract domain from the URL
                            domain_match = re.search(r"https?://([^/]+)", url)
                            if domain_match:
                                domain = domain_match.group(1)
    
                                # If safe domains are defined, check if the domain is included
                                if safe_domains and not any(safe_domain in domain for safe_domain in safe_domains):
                                    issues.append({
                                        'file': file,
                                        'line': line_num,
                                        'message': f"Unknown or insecure webhook domain: {url}",
                                    })
        except Exception as e:
            issues.append({
                'file': file,
                'message': f"Error reading file: {str(e)}"
            })
    
    return issues

def load_gitignore_spec(root_directory):
    """
    Loads the .gitignore file and returns a PathSpec object,
    which can be used to check whether a path should be ignored.
    """
    gitignore_path = os.path.join(root_directory, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as gitignore_file:
            gitignore_lines = gitignore_file.readlines()
        return pathspec.PathSpec.from_lines('gitwildmatch', gitignore_lines)
    return None

def scan_project_for_insecure_webhooks(root_directory):
    """
    Recursively scans the given root directory for Python files and
    checks them for insecure webhook calls.
    
    Files listed in the .gitignore are ignored.
    """
    all_issues = []
    python_files = []
    
    # Load Gitignore specification (if available)
    git_spec = load_gitignore_spec(root_directory)
    
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                
                # Check if the file path (relative to the root directory) is listed in .gitignore
                if git_spec:
                    rel_path = os.path.relpath(file_path, root_directory)
                    if git_spec.match_file(rel_path):
                        # File is ignored
                        continue
                python_files.append(file_path)
    
    issues = check_webhooks(python_files)
    all_issues.extend(issues)
    print(all_issues)
    print(f"Found {len(all_issues)} insecure webhook issues.")
    if len(all_issues) > 0:
        return False
    return True
