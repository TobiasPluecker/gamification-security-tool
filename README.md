# gamification-security-tool

This repository contains the local tool for evaluating a gamification system in a study. The tool requires access to an API and a website to function. Without these components, it will not produce meaningful results. Participants will install and use it during the evaluation.

## Installation & Setup

To use the tool for the study, follow these steps:

# 1. Clone repository
```sh
git clone https://github.com/your-username/gamification-security-tool.git
cd gamification-security-tool/Local_tool
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
Open a terminal and set:
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

# Exercise 2: API Request in Python

**Goal**: Write a Python script that sends a GET request to an API and prints the received data.

---

## Task Instructions

1. **Create a Python Script**  
   - Create a new Python file (e.g., `get_secret_data.py`).  
   - Write code that sends a GET request to the given API URL.

2. **Authentication**  
   - Use the **Bearer Token** for authentication.  
   - Provided token: `12345-abcdef-67890`.

3. **API Endpoint**  
   - Send the GET request to the following endpoint:  
     ```
     https://gamification-api.loca.lt/study/get-secret-data
     ```

4. **Handle the API Response**  
   - Check if the request was successful (`status_code == 200`).  
   - Print the received data (JSON) in the console.

5. **Submission**  
   - Commit your completed script to the provided test repository.

6. **Need Help?**  
   - Check the official API documentation:  
     [Gamification API Docs](https://gamification-api.loca.lt/docs#/Study/get_data_study_get_secret_data_get)
