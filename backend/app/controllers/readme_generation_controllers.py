# backend/app/controllers/readme_generation_controllers.py
from fastapi import APIRouter, HTTPException, Query
from services.readme_generation_service import generate_readme

readme_router = APIRouter()

@readme_router.get("/generate-readme", summary="Generate README.md from Python files in a repo")
async def generate_readme_controller(
    root_dir: str = Query(default="temp_refactored_repo", description="Path to the root directory of the repo"),
    python_version: str = Query(default="3.12", description="Python version used in the repo")
):
    """
    Generate a README.md file based on file-level summaries in the given repository.

    Args:
        root_dir: Path to the local repository root directory.
        python_version: Python version used in the project.

    Returns:
        A dictionary with the generation status.

    Raises:
        HTTPException: If an error occurs during README generation.
    """
    try:
        status = generate_readme(
            root_dir=root_dir,
            python_version=python_version
        )
        return {'status': status}
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
