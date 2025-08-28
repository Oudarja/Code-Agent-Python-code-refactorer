import pytest
import requests
from unittest.mock import patch, MagicMock
from services.git_pr_service import git_pull_request  # Replace 'your_module' with actual module name


@patch("services.git_pr_service.requests.post")
@patch("services.git_pr_service.os.getenv")
def test_git_pull_request_success(mock_getenv, mock_post):
    # Setup mock environment
    mock_getenv.return_value = "dummy_token"

    # Mock successful PR creation response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "https://github.com/user/repo/pull/1"}
    mock_post.return_value = mock_response

    result = git_pull_request("user", "repo", "feature-branch")

    assert result["success"] is True
    assert "https://github.com/user/repo/pull/1" in result["url"]


@patch("services.git_pr_service.requests.post")
@patch("services.git_pr_service.os.getenv")
def test_git_pull_request_already_exists(mock_getenv, mock_post):
    mock_getenv.return_value = "dummy_token"

    # Simulate 422 error with "pull request already exists" message
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.text = "A pull request already exists for this branch."
    mock_post.return_value = mock_response

    result = git_pull_request("user", "repo", "feature-branch")

    assert result["success"] is False
    assert "already exists" in result["message"]


@patch("services.git_pr_service.requests.post")
@patch("services.git_pr_service.os.getenv")
def test_git_pull_request_failure(mock_getenv, mock_post):
    mock_getenv.return_value = "dummy_token"

    # Simulate generic error (e.g., 500)
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        git_pull_request("user", "repo", "feature-branch")

    assert "Failed to create pull request" in str(excinfo.value)
