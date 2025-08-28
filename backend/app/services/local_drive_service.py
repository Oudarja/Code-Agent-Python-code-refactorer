import os
from typing import Dict

BASE_DIR = "temp_refactored_repo"

def get_all_refactored_files(base_path: str = BASE_DIR) -> Dict[str, str]:
    """
    Reads all files under a directory and returns a mapping of relative paths to their contents.

    Args:
        base_path: Directory to read files from.

    Returns:
        A dictionary of file paths and their contents or error messages.
    """
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Directory '{base_path}' does not exist.")

    all_files = {}

    for root, _, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, base_path)

            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    # relative_path = os.path.relpath(full_path, base_path).replace('\\', '/')
                    all_files[os.path.relpath(full_path, base_path).replace('\\', '/')] = f.read()
            except UnicodeDecodeError:
                all_files[relative_path] = "Error: Binary or non-text file. Cannot decode as UTF-8."
            except PermissionError:
                all_files[relative_path] = "Error: Permission denied when reading this file."
            except FileNotFoundError:
                all_files[relative_path] = "Error: File was removed before it could be read."
            except Exception as e:
                all_files[relative_path] = f"Error reading file: {type(e).__name__}: {str(e)}"

    return all_files

def write_all_refactored_files(file_name: str, content: str) -> str:
    """
    Writes content to a file under BASE_DIR using the provided file name.
    Creates intermediate directories if necessary.

    Args:
        file_name (str): File name with optional subdirectories (e.g., 'utils/test.py').
        content (str): The content to write.

    Raises:
        Exception: If write operation fails.
    """
    try:
        file_path = os.path.join(BASE_DIR, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True) 

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return "successfully saved to " + file_path
    except Exception as e:
        raise Exception(f"Error writing to {file_name}: {e}")