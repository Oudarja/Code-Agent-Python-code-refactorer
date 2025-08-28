# Read all .py, .md, and requirements.txt from src/
# Chunk them into logical pieces (e.g., per function/class or sliding window over lines)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from ..utils.github_utils import get_repo_files
from src.utils.github_utils import get_repo_files
import requests


def fetch_target_files(owner, repo, branch):
    all_files = get_repo_files(owner, repo, branch)
    return [f for f in all_files if f.endswith(('.py', '.md', 'requirements.txt'))]

# all_files = get_repo_files("oudarja","Chef-for-you-chatbot-NLP-project-", "main")

# print(all_files)

def get_file_content(owner, repo, branch,filepath):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filepath}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    print("⚠️ Failed to get contents")
    return None



# print(get_file_content())




