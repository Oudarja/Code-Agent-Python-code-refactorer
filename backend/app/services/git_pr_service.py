import os
from typing import Dict
from dotenv import load_dotenv
import requests
from loguru import logger



load_dotenv()



def git_pull_request(
    owner: str,
    repo: str,
    head_branch: str,
    base_branch: str = "main",
    title: str = "CodeAgent Auto PR",
    body: str = "This PR includes automatic refactored code updates."
) -> Dict[str, str | bool]:
    """
    Creates a GitHub pull request from head_branch to base_branch.

    Args:
        owner: GitHub username or organization.
        repo: Repository name.
        head_branch: Source branch for the PR.
        base_branch: Target branch to merge into.
        title: Title of the pull request.
        body: Body/description of the pull request.

    Returns:
        Dict with success status, PR URL (if created), and a message.
    
    Raises:
        Exception: If the PR creation fails for an unexpected reason.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    data = {
        "title": title,
        "head": head_branch,
        "base": base_branch,
        "body": body
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        pr_url = response.json().get("html_url", "N/A")
        return {"success": True, "url": pr_url, "message": f"PR created: {pr_url}"}
    elif response.status_code == 422 and "A pull request already exists" in response.text:
        return {"success": False, "message": "A pull request already exists for this branch."}
    else:
        raise Exception(f"Failed to create pull request: {response.status_code} {response.text}")




