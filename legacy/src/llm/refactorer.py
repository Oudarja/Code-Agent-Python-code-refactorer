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
                    f"You are an expert Python developer, compatibility engineer, and documentation specialist.\n\n"
                    f"Your task is to refactor the provided Python code to ensure full compatibility with Python {python_version}.\n"
                    f"The refactored code must:\n"
                    f"1. Follow best practices and use syntax fully compatible with Python {python_version}.\n"
                    f"2. Replace deprecated or removed syntax, functions, and standard libraries.\n"
                    f"3. Update or replace third-party package imports that are incompatible with Python {python_version}.\n"
                    f"4. Use only packages and versions that are verified to work with Python {python_version}.\n"
                    f"5. Apply appropriate type hints to all function parameters and return types.\n"
                    f"6. Include clean and correct Python docstrings following the Google Python style guide.\n\n"
                    f"When generating docstrings:\n"
                    f"- Clearly describe the purpose of the function or class.\n"
                    f"- List and explain all parameters with their types.\n"
                    f"- Describe the return value and its type.\n"
                    f"- Mention any exceptions the function may raise.\n"
                    f"- Use clear, concise, and professional language.\n\n"
                    f"Additional Guidelines:\n"
                    f"- Do NOT include any explanations, markdown formatting (e.g., triple backticks), or inline comments.\n"
                    f"- Return ONLY the final refactored Python code.\n\n"
                    f"The output must be production-ready, runnable on Python {python_version}, and require no further modification."
                )
            },
            {
                "role": "user",
                "content": f"Refactor this Python code for Python {python_version}:\n\n{code_chunk}"
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


def refactor_large_code(client, code_snippet, st=None, python_version="python3"):
    tokens = estimate_tokens(code_snippet)
    if tokens <= 2000:
        return refactor_code_chunk(client, code_snippet, python_version)

    if st: st.info("🔧 Refactoring code in chunks...")
    chunks = split_code_into_chunks(code_snippet)
    return "\n\n".join([
        extract_code_block(refactor_code_chunk(client, chunk, python_version))
        for chunk in chunks
    ])
