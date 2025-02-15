import os
from bandit.core.config import BanditConfig
from bandit.core.manager import BanditManager
import pathspec

def load_gitignore_spec(root_directory):
    gitignore_path = os.path.join(root_directory, '.gitignore')

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as gitignore_file:
            gitignore_lines = gitignore_file.readlines()
        return pathspec.PathSpec.from_lines('gitwildmatch', gitignore_lines)
    return None

def check_api_security(root_directory):
    print("Checking API security...")
    """
    Uses Bandit to analyze Python files and returns True if no API security issues are found,
    otherwise returns False.
    """
    config = BanditConfig()
    manager = BanditManager(config, "file")

    manager.blacklist = ["B201", "B301", "B303", "B304", "B601", "B701"]

    git_spec = load_gitignore_spec(root_directory)

    python_files = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if git_spec:
            dirnames[:] = [
                d for d in dirnames
                if not git_spec.match_file(os.path.relpath(os.path.join(dirpath, d), root_directory))
            ]
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                if git_spec:
                    rel_path = os.path.relpath(file_path, root_directory)
                    if git_spec.match_file(rel_path):
                        continue
                python_files.append(file_path)

    if not python_files:
        return True

    manager.discover_files(python_files)
    manager.run_tests()

    critical_issues = [
        issue for issue in manager.results
        if issue.severity in ('MEDIUM', 'HIGH') and issue.confidence in ('MEDIUM', 'HIGH')
    ]

    if critical_issues:
        for issue in critical_issues:
            print(f"{issue.fname}:{issue.lineno} - {issue.text} " f"(Severity: {issue.severity}, Confidence: {issue.confidence})")

    return False if critical_issues else True
