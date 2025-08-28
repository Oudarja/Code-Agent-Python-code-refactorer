from urllib.parse import urlparse
from typing import Dict
import requests
from typing import List
from dotenv import load_dotenv
import os
load_dotenv()
def get_owner_and_repo(repo_url: str) -> Dict[str, str]:
    """
    Extracts the owner and repository name from a GitHub URL.

    Example:
        https://github.com/openai/gpt-4 → {"owner": "openai", "repo": "gpt-4"}

    Args:
        repo_url: Full GitHub repository URL.

    Returns:
        Dictionary with 'owner' and 'repo' keys.

    Raises:
        ValueError: If the URL is invalid or not a GitHub URL.
    """
    parsed = urlparse(repo_url)

    # Check if the URL is a GitHub URL
    if parsed.netloc not in ["github.com", "www.github.com"]:
        raise ValueError("URL must be from github.com")

    path_parts = parsed.path.strip("/").split("/")

    # Validate the path
    if len(path_parts) < 2:
        raise ValueError("URL must contain both owner and repository name")

    return {"owner": path_parts[0], "repo": path_parts[1]}

def get_branch_list(owner: str, repo: str) -> List[str]:
    """
    Fetches the list of branch names from a public GitHub repository.
    Args:
        owner (str): GitHub username or organization name.
        repo (str): Repository name.
    Returns:
        List[str]: List of branch names.
    Raises:
        ValueError: If the repository is not found or the API returns an error.
        requests.exceptions.RequestException: If a network error occurs.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return [branch["name"] for branch in res.json()]
        elif res.status_code == 404:
            raise ValueError(f"Repository '{owner}/{repo}' not found (404).")
        else:
            raise ValueError(f"GitHub API error while fetching branches: {res.status_code}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException("Network error while fetching branches") from e


def get_branch_files(owner: str, repo: str, branch: str = "main") -> List[str]:
    """
    Fetches all file paths (blobs) from a specific branch in a GitHub repository.

    Args:
        owner (str): GitHub username or organization name.
        repo (str): Repository name.
        branch (str, optional): The name of the branch to fetch files from. Defaults to "main".

    Returns:
        List[str]: A list of file paths in the given branch.

    Raises:
        ValueError: If the branch or repository is not found, or if the GitHub API returns an error.
        requests.exceptions.RequestException: If a network error occurs.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return [item["path"] for item in res.json()["tree"] if item["type"] == "blob"]
        elif res.status_code == 404:
            raise ValueError(f"Branch '{branch}' not found in repository '{owner}/{repo}' (404).")
        else:
            raise ValueError(f"GitHub API error while fetching files: {res.status_code}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException("Network error while fetching files") from e


def get_github_file_content(
    owner: str,
    repo: str,
    file_path: str,
    branch: str = "main",
    timeout: float = 10.0
) -> str:
    """
    Fetch the raw content of a file from a GitHub repository.

    Args:
        owner (str): GitHub repository owner (user or organization).
        repo (str): GitHub repository name.
        file_path (str): Path to the file within the repository (e.g., "src/utils/helper.py").
        branch (str, optional): Branch name to fetch from. Defaults to "main".
        timeout (float, optional): Seconds to wait for the HTTP response. Defaults to 10.0.

    Returns:
        str: The text content of the requested file.

    Raises:
        GitHubFileNotFoundError: If the file isn't found (HTTP 404).
        GitHubAPIError: If GitHub returns any other non-200 status code.
        RequestException: For network-related issues (connection errors, DNS failures, etc.).
    """
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    try:
        response = requests.get(raw_url, timeout=timeout)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        status = getattr(http_err.response, "status_code", None)
        if status == 404:
            raise FileNotFoundError(
                f"File '{file_path}' not found in {owner}/{repo}@{branch}"
            )
        else:
            raise RuntimeError(
                f"GitHub returned status {status} for URL {raw_url}"
            )
    except requests.RequestException as req_err:
        # Covers network issues, DNS failures, timeouts, etc.
        raise ConnectionError(f"Network error while fetching {raw_url}: {req_err}")

    return response.text



def create_branch(owner: str, repo: str, new_branch: str, from_branch: str = "main") -> bool:
    """
    Creates a new branch in a GitHub repository from a given base branch.

    Args:
        owner: GitHub username or organization.
        repo: Repository name.
        new_branch: Name of the new branch to create.
        from_branch: Name of the base branch to branch from.

    Returns:
        True if the branch was created successfully or already exists.

    Raises:
        Exception: If the base branch is not found or branch creation fails.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}

    # Get the latest commit SHA of the base branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{from_branch}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Failed to get base branch '{from_branch}': {res.status_code} {res.text}")
    
    sha = res.json()["object"]["sha"]

    # Create the new branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    data = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 201:
        return True
    elif res.status_code == 422 and "Reference already exists" in res.text:
        return True  # Branch already exists, so continue
    else:
        raise Exception(f"Failed to create branch '{new_branch}': {res.status_code} {res.text}")

