from pydantic import BaseModel
from typing import List

class DependencyRequest(BaseModel):
    root_dir: str = "temp_refactored_repo"
    python_version: str = "3.12"