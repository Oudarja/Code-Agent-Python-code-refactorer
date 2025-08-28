# backend/app/controllers/git_pr_controller.py
from fastapi import APIRouter, HTTPException
from loguru import logger

from models.model import GitPullMessage
from services.git_pr_service import git_pull_request


git_pr_router=APIRouter() 
@git_pr_router.post("/git-pr",summary="Pull request")
def git_pr_request(data: GitPullMessage):
    """
    Creates a GitHub pull request from one branch to another.

    Args:
        data: GitPullMessage containing repo info and PR metadata.

    Returns:
        A dictionary with success status and pull request URL or error message.

    Raises:
        HTTPException: On failure during pull request creation.
    """
    try:
        message = git_pull_request(data.owner, data.repo, data.head_branch, data.base_branch, data.title, data.body)
        logger.info(message)
        return  message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))