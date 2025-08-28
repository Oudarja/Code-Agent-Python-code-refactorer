# backend/app/controllers/file_analysis_controller.py
from fastapi import APIRouter, HTTPException
from loguru import logger

from models.model import FileContent
from services.file_analysis_service import generate_file_analysis


file_analysis_router=APIRouter()

@file_analysis_router.post("/get-file-analysis",summary="Getting file analysis")
def get_file_analysis(data: FileContent):
    """
    Analyze a single Python file to extract structural or semantic information.

    Args:
        data: FileContent containing file path and code content.

    Returns:
        The result of the file analysis.

    Raises:
        HTTPException: On any failure during processing.
    """
    try:
        # escaped_code = json.dumps( data.code_content) 
        # escaped_code is needed for transmitting as json
        analysis = generate_file_analysis(data.file_path, data.code_content)
        logger.info(analysis)
        return  analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))