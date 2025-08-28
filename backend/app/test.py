import os
from typing import List, Dict, Union
from loguru import logger
import ast

def clean_code_fences(code: str) -> str:
    """Remove Markdown code fences (``` or ```python) from the code string."""
    lines = code.splitlines()
    cleaned = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(cleaned)

def remove_triple_quoted_blocks(code: str) -> str:
    # Remove all triple-quoted string blocks ('''...''' or """...""")
    # so that imports inside them are ignored and unterminated ones don't break parsing.
    lines = code.splitlines()
    cleaned = []
    inside_triple = False
    triple_delim = None

    for line in lines:
        stripped = line.strip()
        # Check if entering or leaving a triple-quoted block
        if not inside_triple:
            if stripped.startswith(('"""', "'''")):
                inside_triple = True
                triple_delim = stripped[:3]
                # If starts and ends on the same line, skip this line only
                if stripped.endswith(triple_delim) and len(stripped) > 3:
                    inside_triple = False
                    triple_delim = None
                continue
            else:
                cleaned.append(line)
        else:
            # Check for closing triple-quote
            if triple_delim in stripped:
                inside_triple = False
                triple_delim = None
            # skip lines inside triple quotes entirely
            continue

    return "\n".join(cleaned)

def extract_imports(file_content: str, file_path: str = "<unknown>"):
    """
    Extract top-level imports from Python code.
    Cleans Markdown fences and ignores triple-quoted blocks.
    """
    imports = []
    file_content = clean_code_fences(file_content)       # remove markdown fences
    file_content = remove_triple_quoted_blocks(file_content)  # drop triple-quoted blocks

    try:
        tree = ast.parse(file_content)
    except SyntaxError as e:
        print(f"Skipping {file_path}: Invalid Python syntax -> {e}")
        return []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            names = ", ".join(alias.name for alias in node.names)
            imports.append(f"from {module} import {names}")

    return imports

if __name__ == "__main__":
    output_file = "imports_summary.txt"
    with open(output_file, "w", encoding="utf-8") as out_f:
        for dirpath, _, filenames in os.walk("temp_refactored_repo"):
            for filename in filenames:
                if not filename.endswith(".py") or filename == "requirements.txt":
                    continue

                file_path = os.path.join(dirpath, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                except Exception as e:
                    print(f"Failed to read file {file_path}: {e}")
                    continue

                try:
                    imports_only = extract_imports(file_content)
                    if imports_only: 
                        out_f.write(f"File: {file_path}\n")
                        out_f.write("\n".join(imports_only))
                        out_f.write("\n\n")  
                except Exception as e:
                    print(f"Failed to extract packages from {file_path}: {e}")

    # with open(r"F:\Internship program\code-agent\backend\app\temp_refactored_repo\apps\coverage_capacity_optimization\cco_example_app.py", "r", encoding="utf-8") as f:
    #     file_content = f.read()
    #     imports_only = extract_imports(file_content)
    #     imports_only = "\n".join(imports_only)
    # logger.info(imports_only)


    # for dirpath, _, filenames in os.walk("temp_refactored_repo"):
    #     # if debug > 50:
    #     #     logger.warning(f"Debug limit reached: {debug} files processed.")
    #     #     break
    #     for filename in filenames:
    #         if not filename.endswith(".py") or filename == "requirements.txt":
    #             logger.warning(f"Skipping non-Python file: {filename}")
    #             continue

    #         file_path = os.path.join(dirpath, filename)

    #         try:
    #             with open(file_path, "r", encoding="utf-8") as f:
    #                 file_content = f.read()
    #                 # debug += 1
    #         except Exception as e:
    #             raise RuntimeError(f"Failed to read file {file_path}: {e}")
    #         try:
    #             imports_only = extract_imports(file_content)
    #             imports_only="\n".join(imports_only)
    #             logger.info(f"Extracted packages from : {file_path}")
    #             logger.info(f"\n")
    #             logger.info(imports_only)
    #             logger.info(f"\n")
    #             logger.info(f"\n")
    #             logger.info(f"\n")
    #         except Exception as e:
    #             raise RuntimeError(f"Failed to extract packages from {file_path}: {e}")
