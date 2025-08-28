import difflib

def generate_code_diff(old_code: str, new_code: str) -> str:
    """
    Generate a unified diff between the original and refactored code.

    Args:
        old_code: Original source code as a string.
        new_code: Refactored source code as a string.

    Returns:
        A string representing the unified diff between the two code versions.
    """
    diff = difflib.unified_diff(
        old_code.strip().splitlines(),
        new_code.strip().splitlines(),
        fromfile='Original',
        tofile='Refactored',
        lineterm=''
    )
    return "\n".join(diff)
