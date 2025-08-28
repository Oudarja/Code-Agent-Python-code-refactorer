# backend/app/controllers/dependency_management_controllers.py
from fastapi import APIRouter, HTTPException
from models.dependency_management_models import DependencyRequest
from services.dependency_management_services import generate_dependencies

dependency_router = APIRouter()

@dependency_router.post("/update-dependencies")
def update_dependencies(payload: DependencyRequest):
    """
    Generate or update project dependencies based on the root directory and Python version.

    Args:
        payload: DependencyRequest containing root_dir and python_version.

    Returns:
        A list or string of resolved dependencies.

    Raises:
        HTTPException: With appropriate status code based on the type of error.
    """
    try:
        return generate_dependencies(
            root_dir=payload.root_dir,
            python_version=payload.python_version
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
