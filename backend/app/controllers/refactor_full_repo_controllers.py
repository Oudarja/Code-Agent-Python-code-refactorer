from fastapi import APIRouter, HTTPException
from models.model import RefactorRequest
from services.refactor_full_repo_service import refactor_all_python_files_in_repo

refactor_api_router = APIRouter()

@refactor_api_router.post("/refactor-python-files", summary="Refactor all Python files in a GitHub repository")
def refactor_python_files(request: RefactorRequest):
    """
    Refactors all Python files in the specified GitHub repository branch.

    Args:
        request: RefactorRequest containing owner, repo, branch, file list, python version, and output dir.

    Returns:
        Dictionary with success status, output directory, and LLM logs.

    Raises:
        HTTPException: If the refactoring process fails.
    """
    try:
        success, output_dir, logs = refactor_all_python_files_in_repo(
            owner=request.owner,
            repo=request.repo,
            branch=request.branch,
            all_files=request.files,
            python_version=request.python_version,
            output_dir=request.output_dir
        )
        return {
            "success": success,
            "output_dir": output_dir,
            "logs": logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
