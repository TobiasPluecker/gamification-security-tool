# gamification-security-tool

This repository contains the local tool for evaluating a gamification system in a study. The tool requires access to an API and a website to function. Without these components, it will not produce meaningful results. Participants will install and use it during the evaluation.

## Installation & Setup

To use the tool for the study, follow these steps:

### 1. Clone repository
```sh
git clone https://github.com/your-username/gamification-security-tool.git
cd gamification-security-tool
pip install -e .
```

### 2. Configure pre-commit hook
In the repository where you want to use the tool, create a `.pre-commit-config.yml` with the following content:
```yaml
repos:
  - repo: local
    hooks:
      - id: local-tool
        name: Pre-Commit Sicherheitscheck
        entry: local_tool
        language: system
        verbose: true
```

### 3. Setting environment variables
Öffnen Sie ein Terminal und führen Sie die folgenden Befehle aus:
```sh
set PYTHONPATH=C:\Path\to\your\gamification-security-tool\installation
set PYTHONIOENCODING=utf-8
```

Create a `.env` file in the `Local_Tool` directory and set the variables mentioned in the `.env.dist`.

### 4. Questions
Ask if you don't know a parameter. 