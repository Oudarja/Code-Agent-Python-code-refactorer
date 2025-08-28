# backend/app/controllers/git_repo_controllers.py
from fastapi import APIRouter, HTTPException, Query
from utils.github_utils import (
    get_owner_and_repo,
    get_github_file_content,
    get_branch_list,
    get_branch_files,
)

git_api_router = APIRouter()

@git_api_router.get("/extract-owner-repo", summary="Extract GitHub Owner and Repo")
def extract_owner_and_repo(repo_url: str = Query(...)):
    """
    Extract the owner and repo name from a GitHub URL.

    Args:
        repo_url: Full GitHub repository URL.

    Returns:
        Dict with 'owner' and 'repo'.
    """
    try:
        return get_owner_and_repo(repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@git_api_router.get("/extract-branch",summary="Extract all branch")
def extract_branchs(owner: str, repo: str):
    """
    Retrieve the list of branches for a given GitHub repository.
    
    Args:
        owner: GitHub username or org.
        repo: Repository name.

    Returns:
        List of branch names.
    """
    try:
        return get_branch_list(owner, repo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@git_api_router.get("/extract-files",summary="Extract all files")
def extract_files(owner: str, repo: str, branch: str):
    """
    Get the list of files in a specified branch of a GitHub repository.

    Args:
        owner: GitHub username or org.
        repo: Repository name.
        branch: Target branch name.

    Returns:
        List of file paths.
    """
    try:
        return get_branch_files(owner, repo, branch)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@git_api_router.get("/get-github-file-content", summary="Get GitHub File Content")
def extract_github_file_content(owner: str, repo: str, file_path: str, branch: str = "main"):
    """
    Fetch the content of a specific file from a GitHub repository branch.

    Args:
        owner: GitHub username or org.
        repo: Repository name.
        file_path: Path to the file in the repo.
        branch: Branch name (default is 'main').

    Returns:
        Raw content of the file as a string.
    """
    try:
        return get_github_file_content(owner, repo, file_path, branch)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
