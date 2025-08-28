# backend/app/controllers/code_diff_controller.py
from fastapi import APIRouter, HTTPException
from loguru import logger

from models.model import CodeDiffRequest
from services.code_diff_service import generate_code_diff


code_diff_router=APIRouter()

@code_diff_router.post("/get-code-diff",summary="Extract code diff")
def get_code_diff(data: CodeDiffRequest):
    """
    Generate a code diff from the original and refactored code.

    Args:
        data: CodeDiffRequest containing old and refactored code.

    Returns:
        A string representing the line-by-line diff.

    Raises:
        HTTPException: If diff generation fails.
    """
    try:
        diff = generate_code_diff(data.old_code, data.refactored_code)
        logger.info(diff)
        return  diff
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))