# backend/app/controllers/git_commit_push_controller.py
from fastapi import APIRouter, HTTPException
from loguru import logger

from models.model import CommitPushMessage
from services.git_commit_push_service import commit_and_push_file_service


commit_push_router=APIRouter() 
@commit_push_router.post("/commit-push",summary="Commit and push refactored file")
def commit_and_push(data: CommitPushMessage):
    """
    Commits and pushes refactored files to a specified branch in the GitHub repository.

    Args:
        data: CommitPushMessage containing repo info, branch names, and commit message.

    Returns:
        Success message or error string.

    Raises:
        HTTPException: On failure during commit or push.
    """
    try:
        message = commit_and_push_file_service(data.owner,data.repo,data.commit_message,data.branch,data.base_branch)
        logger.info(message)
        return  message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))