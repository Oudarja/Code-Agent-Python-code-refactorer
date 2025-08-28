from .groq_client import get_groq_client
from ..utils.token_utils import estimate_tokens, split_code_into_chunks

import re


def clean_refactored_output(text: str) -> str:
    # Remove triple backticks and language tags
    text = re.sub(r"```(?:python)?\n?", "", text)
    text = re.sub(r"\n?```$", "", text)

    # Remove everything after 'Changes:', 'Note:', etc.
    for marker in ["Changes:", "Note:", "Explanation:"]:
        if marker in text:
            text = text.split(marker)[0].strip()

    return text.strip()

def extract_code_block(text):
    """Extracts the first Python code block from a markdown response."""
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def refactor_code_chunk(client, code_chunk, python_version):
    messages = [
        {
            "role": "system",
            "content": (
                f"You are an expert Python developer and compatibility engineer.\n\n"
                f"Your job is to refactor unit test code written in pytest to run cleanly on Python {python_version}. The goal is to:\n"
                f"1. Refactor test code using syntax and testing practices compatible with Python {python_version}.\n"
                f"2. Update deprecated testing methods compatible with Python {python_version}.n"
                f"3. Update standard libraries or testing tools (e.g., `unittest`, `pytest`) to Python {python_version} compatible versions.\n"
                f"4. Do NOT define or recreate any functions that are being tested — import based on old test files.\n"
                f"5. Maintain the original structure and purpose of each test while ensuring compatibility.\n\n"
                f"DO NOT:\n"
                f"- Add explanations, markdown (e.g., triple backticks), or comments.\n"
                f"- Generate docstrings or change the meaning of the test.\n"
                f"- Return anything other than the clean refactored test code.\n\n"
                f"Output must be ONLY the runnable and updated test code for Python {python_version} using pytest."
            )
        },
        {
            "role": "user",
            "content": f"Refactor this test file for Python {python_version}:\n\n{code_chunk}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        max_completion_tokens=4096
    )
    raw_output = response.choices[0].message.content.strip()
    return clean_refactored_output(raw_output)


def refactor_test_file(client, code_snippet, st=None, python_version="python3"):
    tokens = estimate_tokens(code_snippet)
    if tokens <= 2000:
        return refactor_code_chunk(client, code_snippet, python_version)

    if st: st.info("Refactoring code in chunks...")
    chunks = split_code_into_chunks(code_snippet)
    return "\n\n".join([
        extract_code_block(refactor_code_chunk(client, chunk, python_version))
        for chunk in chunks
    ])
