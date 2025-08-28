from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from controllers.git_repo_controllers import git_api_router
from controllers.local_drive_controller import local_drive_router
from controllers.refactor_full_repo_controllers import refactor_api_router
from controllers.readme_generation_controllers import readme_router
from controllers.code_diff_controller import code_diff_router
from controllers.dependency_management_controllers import dependency_router
from controllers.file_analysis_controller import file_analysis_router
from controllers.git_commit_push_controller import commit_push_router
from controllers.git_pr_controller import git_pr_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(git_api_router, prefix="/code-agent-api")
app.include_router(local_drive_router,prefix="/code-agent-api")
app.include_router(refactor_api_router, prefix="/code-agent-api")
app.include_router(readme_router, prefix="/code-agent-api")
app.include_router(code_diff_router ,prefix="/code-agent-api")
app.include_router(dependency_router, prefix="/code-agent-api")
app.include_router(file_analysis_router,prefix="/code-agent-api")
app.include_router(commit_push_router,prefix="/code-agent-api")
app.include_router(git_pr_router,prefix="/code-agent-api")

