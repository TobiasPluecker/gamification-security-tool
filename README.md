# gamification-security-tool

This repository contains the local tool for evaluating a gamification system in a study. The tool requires access to an API and a website to function. Without these components, it will not produce meaningful results. Participants will install and use it during the evaluation.

## Installation & Setup

To use the tool for the study, follow these steps:

### 1. Clone repository
```sh
git clone https://github.com/your-username/gamification-security-tool.git
cd gamification-security-tool/local_tool
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



## Now you can start with the study
Please complete the tasks as quickly as possible. Try to behave as you would when solving similar tasks in your daily life.

### Steps before starting the tasks:

Access the Gamification API
- visit: https://gamification-api.loca.lt
- Enter the same password as before to gain access. No further actions are required here.

Access the Gamification Website:
- Go to: https://gamification-website.loca.lt/
- You will need a password to access the site. Please request the password before proceeding.
- Once logged in, use the key 0ef32462-d999-4a7c-be73-5e97e2caa95e to join a project.
- Choose a name for yourself within the project.

In the Test Repository:
```sh
pip install pre_commit
```

```sh
pre-commit install
```

After completing these steps, you can proceed with the tasks.

### Exercise 1: Introduction
Write a "Hello, World!" program in a compiled programming language of your choice (e.g., C, C++, Java, Go, Rust). Ensure that the code is compiled into an executable file. Then, commit and push the code to the Git repository in a way that you would normally do in your daily workflow. The file should be placed in a directory named "exercise_1" or a similar structure you would typically use.

### Exercise 2: API Request in Python
Goal: Write a Python script to send an API request and print the received data.

Instructions:
- Use Python to send a GET request.
- Authenticate with the provided Bearer Token.
- API Endpoint: https://gamification-api.loca.lt/study/get-secret-data
- Bearer Token: 123456789abcdef
- Submission: Commit the script to the given test repository.
- If you need help: https://gamification-api.loca.lt/docs#/Study/get_data_study_get_secret_data_get
