import subprocess
import tempfile
import os
import sys
import shutil


def setup_virtualenv_and_install_requirements(requirements_text: str, python_version: str = None):
    if python_version:
        python_executable = shutil.which(f"python{python_version}")
        if not python_executable:
            msg = f"Python {python_version} not found. Falling back to current Python: {sys.executable}"
            python_executable = sys.executable
        else:
            msg = f"Using Python {python_version}: {python_executable}"
    else:
        python_executable = sys.executable
        msg = f"Using current Python: {python_executable}"

    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = os.path.join(temp_dir, "venv")
        requirements_file = os.path.join(temp_dir, "requirements.txt")

        # Write the requirements.txt
        try:
            with open(requirements_file, "w", encoding="utf-8") as f:
                f.write(requirements_text)
        except Exception as e:
            return False, f"Failed to write requirements.txt: {str(e)}", []

        # Step 1: Create virtual environment
        try:
            subprocess.run([python_executable, "-m", "venv", venv_dir], check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to create virtual environment.", []

        # Resolve paths
        pip_path = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip.exe")
        python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")

        # Step 2: Ensure pip is installed
        try:
            subprocess.run([python_path, "-m", "ensurepip", "--upgrade"], check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to bootstrap pip in the virtual environment.", []

        # Step 3: Upgrade pip, setuptools, wheel using python -m pip
        try:
            subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to upgrade pip/setuptools/wheel: {e}", []

        # Step 4: Install distlib as an alternative to distutils
        try:
            subprocess.run([pip_path, "install", "distlib"], check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to install distlib (Python 3.12 compatibility).", []

        # Step 5: Install requirements using only wheels (no building from source)
        try:
            subprocess.run(
                [pip_path, "install", "--only-binary=:all:", "-r", requirements_file],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or "Unknown error during dependency installation"
            return False, f"Failed to install packages:\n\n{error_msg}", []

        # Step 6: List installed packages
        try:
            result = subprocess.run([pip_path, "list"], stdout=subprocess.PIPE, check=True, text=True)
            installed_packages = result.stdout.strip().splitlines()[2:]
        except subprocess.CalledProcessError:
            installed_packages = []

        return True, f"{msg}\nEnvironment setup and installation successful.", installed_packages

