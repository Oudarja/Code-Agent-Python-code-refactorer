import os
import pytest
from unittest.mock import patch, MagicMock

from services.git_commit_push_service import commit_and_push_file_service

# Mock get_all_refactored_files to avoid actual file reads
def mock_get_all_refactored_files(base_path):
    return {
        "file1.py": "print('Hello World')",
        "file2.txt": "Some text content"
    }

# Mock create_branch to just return True
def mock_create_branch(owner, repo, branch, from_branch="main"):
    return True

@pytest.fixture(autouse=True)
def set_env_token():
    os.environ["GITHUB_TOKEN"] = "fake_token"
    yield
    del os.environ["GITHUB_TOKEN"]

@patch("services.git_commit_push_service.get_all_refactored_files", side_effect=mock_get_all_refactored_files)
@patch("services.git_commit_push_service.create_branch", side_effect=mock_create_branch)
@patch("services.git_commit_push_service.requests.put")
@patch("services.git_commit_push_service.requests.get")
def test_commit_and_push(mock_get, mock_put, mock_create_branch_func, mock_get_files):
    # Mock GET request to simulate that file does not already exist (so no sha needed)
    mock_get.return_value = MagicMock(status_code=404, json=lambda: {})

    # Mock PUT request to simulate successful commit
    mock_put.return_value = MagicMock(status_code=201, text="Success")

    result = commit_and_push_file_service(
        owner="test_owner",
        repo="test_repo",
        commit_message="Test commit",
        branch="test_branch",
        base_branch="main"
    )

    assert result == "Committed all file successfully"
    mock_create_branch_func.assert_called_once_with("test_owner", "test_repo", "test_branch", from_branch="main")
