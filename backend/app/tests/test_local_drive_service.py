# To create temporary directories/files for testing or temporary 
# storage that get automatically cleaned up.
import tempfile
# To copy, move, or delete entire directories, useful for cleaning
#  up after tests or working with file trees.
import shutil
import pytest
import os
import sys

from requests import RequestException, HTTPError
from services.local_drive_service import get_all_refactored_files,write_all_refactored_files, BASE_DIR 

def test_get_all_refactored_files_reads_text_and_binary_files():
    # Create a temporary directory and sample files
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a text file
        text_file_path = os.path.join(temp_dir, "sample.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write("This is a test file.")

        # Create a Python file
        py_file_path = os.path.join(temp_dir, "script.py")
        with open(py_file_path, "w", encoding="utf-8") as f:
            f.write("print('Hello, World!')")

        # Create a binary file (e.g., image header bytes)
        binary_file_path = os.path.join(temp_dir, "image.png")
        with open(binary_file_path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

        # Run the function
        result = get_all_refactored_files(base_path=temp_dir)

        # Assertions
        assert "sample.txt" in result
        assert result["sample.txt"] == "This is a test file."

        assert "script.py" in result
        assert result["script.py"] == "print('Hello, World!')"

        assert "image.png" in result
        assert "Error" in result["image.png"] or "PNG" in result["image.png"]

    finally:
        shutil.rmtree(temp_dir)

def test_get_all_refactored_files_directory_not_found():
    with pytest.raises(FileNotFoundError) as exc_info:
        get_all_refactored_files(base_path="non_existing_directory")
    assert "does not exist" in str(exc_info.value)


# ---------------------test for write_all_refactored_files----------------


@pytest.fixture(autouse=True)
def clean_base_dir():
    # Clean up before and after each test
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    yield
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)

def test_write_simple_file():
    file_name = "testfile.py"
    content = "print('Hello, world!')"
    write_all_refactored_files(file_name, content)

    file_path = os.path.join(BASE_DIR, file_name)
    assert os.path.exists(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        assert f.read() == content

def test_write_nested_file():
    file_name = "utils/helpers/test_helper.py"
    content = "def test(): pass"
    write_all_refactored_files(file_name, content)

    file_path = os.path.join(BASE_DIR, file_name)
    assert os.path.exists(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        assert f.read() == content

def test_write_empty_content():
    file_name = "empty.py"
    content = ""
    write_all_refactored_files(file_name, content)

    file_path = os.path.join(BASE_DIR, file_name)
    assert os.path.exists(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        assert f.read() == content

def test_write_invalid_path_raises_exception(monkeypatch):
    def broken_makedirs(*args, **kwargs):
        raise PermissionError("No permission to create dir")

    monkeypatch.setattr(os, "makedirs", broken_makedirs)

    with pytest.raises(Exception) as e:
        write_all_refactored_files("fail.py", "data")
    assert "Error writing to fail.py" in str(e.value)





