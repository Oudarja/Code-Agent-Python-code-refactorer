import os
import base64
import requests
from dotenv import load_dotenv
from loguru import logger

from utils.github_utils import create_branch
from services.local_drive_service import get_all_refactored_files

load_dotenv()

def commit_and_push_file_service(
    owner: str,
    repo: str,
    commit_message: str = "Auto commit",
    branch: str = "auto-refactored-branch",
    base_branch: str = "main"
) -> str:
    """
    Commits and pushes all files from 'temp_refactored_repo' to the specified GitHub branch.

    If the branch doesn't exist, it is created from the base branch. Each file is created or 
    updated in the repo via the GitHub API.

    Args:
        owner: GitHub username or org.
        repo: Repository name.
        commit_message: Message to use for commits.
        branch: Target branch name.
        base_branch: Source branch to create target branch from if needed.

    Returns:
        Success message or error string.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}
    base_path = "temp_refactored_repo"

    try:
        # Ensure branch exists (create if needed)
        create_branch(owner, repo, branch, from_branch=base_branch)
    except Exception as e:
        logger.error(f"Failed to create or verify branch '{branch}': {e}")
        return f"Failed to create or verify branch '{branch}': {e}"

    try:
        # Get all files & contents from helper
        all_files = get_all_refactored_files(base_path)
    except Exception as e:
        logger.error(f"Failed to get files from '{base_path}': {e}")
        return f"Failed to get files from '{base_path}': {e}"

    for file_path, content in all_files.items():
        try:
            if content.startswith("Error:"):
                logger.warning(f"Skipping {file_path} due to read error: {content}")
                continue

            file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

            # Check if file exists on GitHub to get sha for update
            res = requests.get(f"{file_url}?ref={branch}", headers=headers)
            sha = res.json().get("sha") if res.status_code == 200 else None

            data = {
                "message": f"{commit_message}: {file_path}",
                "content": base64.b64encode(content.encode()).decode(),
                "branch": branch
            }
            if sha:
                data["sha"] = sha

            put_res = requests.put(file_url, headers=headers, json=data)

            if put_res.status_code in [200, 201]:
                logger.info(f"Committed {file_path} successfully.")
            else:
                logger.error(f"Failed to commit {file_path}: {put_res.status_code} {put_res.text}")
                return f"Failed to commit {file_path}: {put_res.status_code} {put_res.text}"
        except Exception as e:
            logger.error(f"Exception committing {file_path}: {e}")
            return f"Exception committing {file_path}: {e}"
        
    return "Committed all file successfully"
