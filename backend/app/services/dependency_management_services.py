import os
import sys 
import re
import tempfile
import shutil
import subprocess
from typing import List, Dict, Union
from utils.llm_utils.dependency_generation_prompt import get_packages, merge_packages
from loguru import logger

def clean_requirements_output(raw_text: str) -> str:
    """
    Cleans raw dependency output by extracting valid Python package names.

    Rules:
    - Removes lines with spaces or inline comments.
    - Keeps only alphanumeric package names (including underscore, hyphen).
    - Ignores any text before or after the package list.

    Args:
        raw_text (str): Raw multiline string containing package info.

    Returns:
        str: Cleaned newline-separated list of package names.
    """
    lines = raw_text.strip().splitlines()
    cleaned = []

    for line in lines:
        # Remove inline comments
        line = line.split("#")[0].strip()
        # Ignore empty or space-containing lines
        if line and re.match(r"^[a-zA-Z0-9_\-]+$", line):
            cleaned.append(line)

    return "\n".join(cleaned)

def setup_virtualenv_and_install_requirements(
    requirements_text: str,
    python_version: str = None,
    refactor_dir: str = 'temp_refactored_repo'
) -> Dict[str, Union[bool, str, List[str]]]:
    """
    Creates a temporary virtual environment, installs packages, and writes
    the frozen package list into a requirements.txt file inside refactor_dir.

    Returns:
        Dict with keys:
        - success: True/False
        - message: Description of the result
        - installed_packages: List of packages installed via pip freeze
    """
    # Resolve Python interpreter
    logger.info("Setting up virtual environment...")
    if python_version:
        python_executable = shutil.which(f"python{python_version}")
        if not python_executable:
            python_executable = sys.executable
            msg = f"Python {python_version} not found. Using current Python: {python_executable}"
        else:
            msg = f"Using Python {python_version}: {python_executable}"
    else:
        python_executable = sys.executable
        msg = f"Using current Python: {python_executable}"

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            venv_dir = os.path.join(temp_dir, "venv")
            requirements_file = os.path.join(temp_dir, "requirements.txt")

            # Step 1: Write requirements
            try:
                with open(requirements_file, "w", encoding="utf-8") as f:
                    f.write(requirements_text)
            except Exception as e:
                raise RuntimeError(f"Failed to write requirements.txt: {e}")

            # Step 2: Create virtual environment
            try:
                subprocess.run([python_executable, "-m", "venv", venv_dir], check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to create virtual environment: {e}")

            pip_path = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip.exe")
            python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")

            # Step 3: Bootstrap pip
            try:
                subprocess.run([python_path, "-m", "ensurepip", "--upgrade"], check=True)
            except subprocess.CalledProcessError:
                raise RuntimeError("Failed to bootstrap pip in the virtual environment.")

            # Step 4: Install dependencies
            try:
                subprocess.run(
                    [pip_path, "install", "--only-binary=:all:", "-r", requirements_file],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr or e.stdout or str(e)
                raise RuntimeError(f"Failed to install packages:\n{error_msg}")

            # Step 5: Freeze installed packages
            try:
                result = subprocess.run([pip_path, "freeze"], stdout=subprocess.PIPE, check=True, text=True)
                installed_packages = result.stdout.strip().splitlines()
            except subprocess.CalledProcessError:
                installed_packages = []

            # Step 6: Save frozen requirements
            try:
                os.makedirs(refactor_dir, exist_ok=True)
                final_reqs_path = os.path.join(refactor_dir, "requirements.txt")
                with open(final_reqs_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(installed_packages))
            except Exception as e:
                raise RuntimeError(f"Failed to save frozen requirements.txt: {e}")

            return {
                "success": True,
                "message": f"{msg}\nEnvironment setup and installation successful.",
                "installed_packages": "\n".join(installed_packages)
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {e}",
            "installed_packages": ''
        }



def generate_dependencies(
    root_dir: str = 'temp_refactored_repo',
    python_version: str = "3.12"
) -> Dict[str, str]:
    """
    Scans Python files in a directory, extracts dependencies using LLM,
    installs them in a temporary virtual environment, and writes the 
    frozen requirements to `requirements.txt` in the same directory.

    Returns:
        dict: {
            "message": str,
            "installed_packages": List[str]
        }

    Raises:
        FileNotFoundError: If the root_dir does not exist.
        RuntimeError: If reading files, LLM extraction, or env setup fails.
        ValueError: If no valid Python files found.
    """
    key_index = 0  # Start with the first API key
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Directory '{root_dir}' does not exist.")

    package_summary: Dict[str, str] = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".py") or filename == "requirements.txt":
                logger.warning(f"Skipping non-Python file: {filename}")
                continue

            file_path = os.path.join(dirpath, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except Exception as e:
                raise RuntimeError(f"Failed to read file {file_path}: {e}")

            try:
                packages, key_index = get_packages(file_content, python_version, key_index)
                relative_path = os.path.relpath(file_path, root_dir)
                package_summary[relative_path] = packages
                logger.info(f"Extracted packages from : {relative_path}")
            except Exception as e:
                raise RuntimeError(f"Failed to extract packages from {file_path}: {e}")

    if not package_summary:
        raise ValueError(f"No valid Python files found in directory '{root_dir}'.")

    try:
        merged = merge_packages(package_summary, python_version)
        cleaned = clean_requirements_output(merged)
    except Exception as e:
        raise RuntimeError(f"Failed to merge and clean dependencies: {e}")

    try:
        response = setup_virtualenv_and_install_requirements(
            requirements_text=cleaned,
            python_version=python_version,
            refactor_dir=root_dir
        )
        if not response["success"]:
            raise RuntimeError(f"Virtualenv setup failed: {response['message']}")
        logger.info("Virtual environment setup and dependency validation completed successfully.")
        return {
            "message": response["message"],
            "installed_packages": response["installed_packages"]
        }

    except Exception as e:
        raise RuntimeError(f"Environment setup error: {e}")
        