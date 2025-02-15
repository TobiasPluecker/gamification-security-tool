from setuptools import setup, find_packages

setup(
    name="local_tool",
    version="1.0",
    description="Ein Pre-Commit-Sicherheitscheck-Tool",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "detect-secrets",
        "bandit",
        "pathspec",
        "dotenv",
    ],
    entry_points={
        "console_scripts": [
            "local_tool=Local_Tool.main:main",
        ]
    },
)
