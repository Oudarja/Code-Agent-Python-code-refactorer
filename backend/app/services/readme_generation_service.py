import os
from typing import List  , Dict
from utils.llm_utils.readme_generation_prompt import generate_readme_from_repo_summary, file_summary 
from loguru import logger

def generate_repo_summary(root_dir: str, files_path: List[str]) -> Dict[str, str]:
    """
    Generates summaries for a list of Python files in a repository.

    Args:
        root_dir: Root directory of the repository.
        files_path: List of relative file paths to summarize. 

    Returns:
        A dictionary mapping each file path to its summary or an error message.
    """
    repo_summary = {}
    key_index = 1  # Start with the first API key

    for file_path in files_path:
        full_path = os.path.join(root_dir, file_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            repo_summary[file_path], key_index = file_summary(file_content, file_path, key_index)
            logger.info(f"Summarized file: {file_path}")
        except Exception as e:
            repo_summary[file_path] = f"Error reading or summarizing file: {e}"

    return repo_summary  # ✅ Return the raw dictionary, not a formatted string


def generate_readme(root_dir: str = "temp_refactored_repo", python_version: str = "3.12") -> str:
    """
    Generates a professional README.md for the full repository using an LLM
    and saves it to the root directory.

    Args:
        root_dir (str): Path to the root directory of the repository.
        python_version (str): Python version to target in README context.

    Returns:
        str: Generated README content.

    Raises:
        RuntimeError: If the README generation process fails.
    """
    try: 
        # Recursively collect all .py files under root_dir
        files_path = []
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".py"):
                    full_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(full_path, root_dir)
                    files_path.append(relative_path)

        # Generate summary and README content
        repo_summary = generate_repo_summary(root_dir, files_path)
        logger.info("Generated repository summary successfully.")
        readme_content = generate_readme_from_repo_summary(repo_summary, python_version)

        # Save README.md to root_dir
        readme_path = os.path.join(root_dir, "README.md")
        os.makedirs(root_dir, exist_ok=True)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        return f"Generated README.md successfully and saved to {readme_path}"
    except Exception as e:
        raise RuntimeError(f"Failed to generate and save README: {str(e)}")
