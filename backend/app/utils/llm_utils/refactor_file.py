import re 
import time 
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.text_splitter import PythonCodeTextSplitter

from utils.llm_utils.create_groq_client import get_groq_client
from loguru import logger


def clean_llm_code_output(text: str) -> str:
    """
    Extracts and returns the code inside the first ```python ...``` block 
    from LLM-generated output. Falls back to any ```...``` block if needed.

    Args:
        text: LLM-generated string containing markdown-formatted code.

    Returns:
        Extracted code string, or original text if no code block is found.
    """
    # Normalize line endings and strip leading/trailing space
    text = text.strip().replace("\r\n", "\n").replace("\r", "\n")

    # Try to extract from the first ```python ... ``` block
    match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: try any ``` ... ``` block (without language specifier)
    match = re.search(r"```\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    return text  # Nothing found


def refactor_code_or_test_file(
    code: str,
    file_path: str,
    python_version: str = "3.12",
    file_type: str = "code",
    key_index = 1
) -> str:
    """    Refactors a Python code or test file using LLM.
    Args:
        code (str): The original code content.
        file_path (str): The path of the file being refactored.
        python_version (str): Target Python version for refactoring.
        file_type (str): Type of file - 'code' or 'test'.
    Returns:
        str: The refactored code content.  
    """
    
    llm = get_groq_client(key_index)

    # Prompts
    system_prompt = SystemMessage(content="You are a powerful code refactorer and version upgrader.")

    init_prompt = f"""
        I will send you a large {file_type} file by chunking. File name is : {file_path}. you just read all the chunks also remember class and function information. whenever I will say that all chunks are provided, then you should refactor the full code file. No need to say anything, you can say just next.. ok?
    """

    if file_type == "code":
        final_instruction = f"""
            You now have the full code.

            Your task:
            - Refactor the entire code to be compatible with **Python {python_version}**.
            - Ensure proper indentation and clean formatting.
            - Add missing **docstrings** and **type hints** where applicable.
            - Maintain clarity and structure throughout.

            Important:
            - Output only valid Python code.
            - No explanations, comments, or markdown.
            - Do not stop until the **entire updated code** is provided.
            """
    else:
        final_instruction = f"""
            You now have the full test file.

            Your task:
            - Refactor and updated the full content to **Python {python_version}**.
            - Follow best practices (`pytest` or `unittest` as applicable).
            - Add docstrings and type hints.
            - Make test names clear and meaningful.

            Important:
            - Output only the final Python test code.
            - No comments, markdown, or summaries.
            - Do not stop until the **entire test file** is refactored.
            """

    text_splitter = PythonCodeTextSplitter(chunk_size=100000, chunk_overlap=0)
    chunks = text_splitter.split_text(code)
    chunks.insert(0, init_prompt)
    chunks.append(final_instruction)

    messages = [system_prompt]
    final_output = ''
    
    for chunk in chunks:
        messages.append(HumanMessage(content=chunk))
        while True:
            try:
                logger.info(f"Sending chunk to LLM:...")  
                response = llm.invoke(messages) 
                break  # Exit loop on success
            except Exception as e:
                msg = str(e)
                key_index = (key_index + 1) % 4  # Rotate through API keys
                logger.error(f"Error invoking LLM: {msg}. Switching to API key index {key_index}...")
                llm = get_groq_client(key_index)  # Reinitialize client
                

        messages.append(AIMessage(content=response.content))
        final_output = response.content
    return clean_llm_code_output(final_output), key_index
