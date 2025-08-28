from pydantic import BaseModel,Field, field_validator
from typing import List, Optional 

class RefactorRequest(BaseModel):
    owner: str
    repo: str
    branch: str
    files: List[str]
    python_version: str
    output_dir: Optional[str] = "temp_refactored_repo"


class CodeDiffRequest(BaseModel):
    old_code: str
    refactored_code: str


class FileContent(BaseModel):
    code_content:str
    file_path:str


class CommitPushMessage(BaseModel):
    owner: str
    repo: str
    commit_message: str
    branch: str = "auto-refactored-branch"
    base_branch: str = "main"

    @field_validator("branch", "base_branch", mode="before")
    @classmethod
    def strip_or_default(cls, v, info):
        if not v or not str(v).strip():
            #fallback to default value
            return info.field.default  
        return str(v).strip()



class GitPullMessage(BaseModel):
    owner: str
    repo: str
    head_branch: str = "auto-refactored-branch"
    base_branch: str = "main"
    title: str = "CodeAgent Auto PR"
    body: str = "This PR includes automatic refactored code updates."

    @field_validator("head_branch", "base_branch", "title", "body", mode="before")
    @classmethod
    def strip_or_default(cls, v, info):
        if not v or not str(v).strip():
            return info.field.default
        return str(v).strip()

class FileWriteRequest(BaseModel):
    file_name: str
    content: str

class RefactorRequest(BaseModel):
    owner: str
    repo: str
    branch: str
    files: List[str]
    python_version: str
    output_dir: Optional[str] = "temp_refactored_repo"