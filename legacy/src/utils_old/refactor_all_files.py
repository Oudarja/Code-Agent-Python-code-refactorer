import os
from pathlib import Path
from collections import defaultdict
from src.utils.github_utils import get_repo_files, download_file
from src.llm.refactorer import refactor_large_code
from src.llm.refactor_test_file import refactor_test_file
from src.llm.update_dependencies import generate_updated_dependencies
from src.llm.readme_generation import generate_readme
from src.llm.packages_handling import generate_dependencies

def refactor_all_python_files_in_repo(client, owner, repo, branch, python_version, st, output_dir="temp", progress_callback=None):
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    files_path = []

    refactor_log = []  # Collects logs for UI/debug 

    try:
        all_files = get_repo_files(owner, repo, branch)
        total_files = len(all_files)


        for idx, file_path in enumerate(all_files):
            files_path.append(file_path)
            file_ext = os.path.splitext(file_path)[1]
            content = download_file(owner, repo, file_path, branch)

            if file_ext == ".py":
                try:
                    is_test_file = (
                        "tests" in Path(file_path).parts
                        or Path(file_path).name.startswith("test_")
                    )

                    if is_test_file:
                        refactored = refactor_test_file(client, content, st, python_version)
                    else:
                        refactored = refactor_large_code(client, content, st, python_version)

                    refactor_log.append(f"[✓] Refactored: {file_path}")

                except Exception as err:
                    refactored = content
                    refactor_log.append(f"[x] Failed to refactor {file_path}: {err}")
            else:
                refactored = content

            full_path = output_root / Path(file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(refactored)

            if progress_callback:
                progress_callback((idx + 1) / total_files)
        
        # ---------- Generate requirements.txt ----------
        # try:
        #     requirements_content = generate_dependencies(
        #         client=client,
        #         root_dir=output_root,
        #         files_path=files_path,
        #         python_version=python_version
        #     )
        #     requirements_path = output_root / "requirements.txt"
        #     with open(requirements_path, "w", encoding="utf-8") as f:
        #         f.write(requirements_content)
        #     refactor_log.append("[✓] Generated requirements.txt")
        # except Exception as e:
        #     refactor_log.append(f"[✗] Failed to generate requirements.txt: {e}")

        
        return True, str(output_root), refactor_log

    except Exception as e:
        return False, None, [f"Error: {e}"]
