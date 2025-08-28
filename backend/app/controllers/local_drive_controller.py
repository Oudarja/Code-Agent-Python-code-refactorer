# backend/app/controllers/local_drive_controller.py
from fastapi import APIRouter, HTTPException
from models.model import FileWriteRequest
from services.local_drive_service import (
    get_all_refactored_files,
    write_all_refactored_files,
)

local_drive_router = APIRouter()

@local_drive_router.get("/get-refactored-content",summary="Get content from local drive")
def get_refactored_files():
    """
    Retrieve all refactored files from the local drive.

    Returns:
        A dictionary with file paths and their contents.

    Raises:
        HTTPException: If the directory is missing or an unexpected error occurs.
    """
    try:
        files = get_all_refactored_files()
        return {"status": "success", "files": files}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@local_drive_router.post("/write-refactored-content", summary="Write content to local drive")
def write_refactored_files(request: FileWriteRequest):
    """
    Write content to a local file, creating intermediate folders if needed.

    Args:
        request: FileWriteRequest with file name and content.

    Returns:
        Success message and written file path.

    Raises:
        HTTPException: If write fails or file is not found.
    """
    try:
        files = write_all_refactored_files(request.file_name, request.content)
        return {"status": "success", "files": files}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")