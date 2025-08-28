import pytest
import requests
import os
import sys
from requests import RequestException, HTTPError
# from utils.github_utils import get_owner_and_repo, get_github_file_content

from unittest.mock import patch, Mock

# Ensure 'src' is in sys.path for import
from utils.github_utils import (
    get_owner_and_repo, 
    get_github_file_content,
    get_branch_list,
    get_branch_files
    )

#——— Tests for get_owner_and_repo ——————————————————

@pytest.mark.parametrize("url, expected", [
    ("https://github.com/openai/gpt-4", {"owner": "openai", "repo": "gpt-4"}),
    ("https://www.github.com/foo/bar",   {"owner": "foo",    "repo": "bar"}),
])
def test_get_owner_and_repo_valid(url, expected):
    assert get_owner_and_repo(url) == expected

@pytest.mark.parametrize("url", [
    "https://gitlab.com/openai/gpt-4",   # wrong domain
    "https://github.com/openai",         # missing repo
    "not a url",                         # malformatted
])
def test_get_owner_and_repo_invalid(url):
    with pytest.raises(ValueError):
        get_owner_and_repo(url)


#——— Helpers for mocking responses ——————————————————

class DummyResponse:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        if self.status_code != 200:
            err = HTTPError(f"Status {self.status_code}")
            err.response = self
            raise err


#——— Tests for get_github_file_content —————————————

def test_get_github_file_content_success(monkeypatch):
    dummy = DummyResponse(200, text="hello world")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: dummy)

    content = get_github_file_content("owner", "repo", "path/to/file.txt")
    assert content == "hello world"

def test_get_github_file_content_not_found(monkeypatch):
    dummy = DummyResponse(404)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: dummy)

    with pytest.raises(FileNotFoundError) as exc:
        get_github_file_content("o", "r", "missing.txt")
    assert "not found" in str(exc.value).lower()

def test_get_github_file_content_api_error(monkeypatch):
    dummy = DummyResponse(500)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: dummy)

    with pytest.raises(RuntimeError) as exc:
        get_github_file_content("o", "r", "file.txt")
    assert "status 500" in str(exc.value).lower()

def test_get_github_file_content_network_error(monkeypatch):
    def raise_req(*args, **kwargs):
        raise RequestException("connection broke")
    monkeypatch.setattr(requests, "get", raise_req)

    with pytest.raises(ConnectionError) as exc:
        get_github_file_content("o", "r", "file.txt")
    assert "network error" in str(exc.value).lower()


#------Tests for get_branch_list and get_branch_files-----------------

@patch("utils.github_utils.requests.get")
def test_get_branch_list_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "main"}, {"name": "dev"}]
    mock_get.return_value = mock_response

    branches = get_branch_list("user", "repo")
    assert branches == ["main", "dev"]


@patch("utils.github_utils.requests.get")
def test_get_branch_list_404(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Repository 'user/repo' not found"):
        get_branch_list("user", "repo")


@patch("utils.github_utils.requests.get")
def test_get_branch_list_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network down")
    
    with pytest.raises(requests.exceptions.RequestException):
        get_branch_list("user", "repo")


# --- Test get_branch_files ---
@patch("utils.github_utils.requests.get")
def test_get_branch_files_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "tree": [
            {"path": "README.md", "type": "blob"},
            {"path": "src/main.py", "type": "blob"},
            {"path": "src", "type": "tree"}
        ]
    }
    mock_get.return_value = mock_response

    files = get_branch_files("user", "repo", "main")
    assert files == ["README.md", "src/main.py"]


@patch("utils.github_utils.requests.get")
def test_get_branch_files_404(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Branch 'main' not found"):
        get_branch_files("user", "repo", "main")


@patch("utils.github_utils.requests.get")
def test_get_branch_files_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Timeout")

    with pytest.raises(requests.exceptions.RequestException):
        get_branch_files("user", "repo", "main")

