import os 
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from utils.github_utils import get_github_file_content
from utils.llm_utils.refactor_file import refactor_code_or_test_file
from loguru import logger

def refactor_all_python_files_in_repo(
    owner: str,
    repo: str,
    branch: str,
    all_files: List[str],
    python_version: str,
    output_dir: str = "temp_refactored_repo"
) -> Tuple[bool, Optional[str], List[str]]:
    """
    Refactors all Python files in a GitHub repository using LLM.

    Args:
        owner: GitHub repo owner.
        repo: GitHub repo name.
        branch: Branch name to fetch files from.
        all_files: List of file paths in the repo.
        python_version: Target Python version for refactoring.
        output_dir: Local output directory for refactored files.

    Returns:
        A tuple: (success_flag, output_dir_path or None, log_messages)
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    refactor_log: List[str] = []
    key_index = 1

    try:
        for file_path in all_files:
            file_ext = os.path.splitext(file_path)[1]
            try:
                content = get_github_file_content(owner, repo, file_path, branch)

                if file_ext == ".py":
                    is_test_file = (
                        "tests" in Path(file_path).parts or
                        Path(file_path).name.startswith("test_")
                    )
                    file_type = 'test' if is_test_file else 'code'

                    refactored, key_index = refactor_code_or_test_file(
                        code=content,
                        file_path=file_path,
                        python_version=python_version,
                        file_type=file_type,
                        key_index=key_index
                    )
                    refactor_log.append(f"[✓] Refactored: {file_path}")
                else:
                    refactored = content
                    refactor_log.append(f"[-] Skipped (not .py): {file_path}")
                logger.info(f"Processed {refactor_log[-1]} successfully.")

            except Exception as err:
                refactored = ""
                refactor_log.append(f"[x] Failed {file_path}: {err}")

            # Write to output
            full_path = output_root / Path(file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(refactored)

        return True, str(output_root), refactor_log

    except Exception as e:
        return False, None, [f"[!] Unexpected error: {e}"]
