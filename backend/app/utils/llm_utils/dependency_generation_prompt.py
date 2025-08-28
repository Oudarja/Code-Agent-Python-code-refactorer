import re
import time
from typing import List, Dict
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.text_splitter import PythonCodeTextSplitter
from utils.llm_utils.create_groq_client import get_groq_client
from loguru import logger

def get_packages(file_content: str, python_version: str = '3.12', key_index: int = 0) -> str:
    """
    Extract top-level Python packages (without versions) required by the given source code.

    Sends code in chunks to an LLM, which analyzes the imports and returns necessary packages.
    Handles rate limiting and retries if needed.

    Args:
        file_content (str): Full source code as a string.

    Returns:
        str: Space-separated list of package names suitable for installation.
    """

    llm = get_groq_client(key_index)
    # Prompts
    system_prompt = SystemMessage(content="You are a powerfull packages manager.")

    init_prompt = f"""
        I will send you a large file by chunking. You just read all the chunks also remember the import modules. 
        whenever I will say that all chunks are provided, then you should write the packages without version that are required for the full code of python version {python_version}.
        No need to say anything, you can say just next.. ok?
    """

    final_instruction = f"""
        All chunks are provided. Now analyze full code and produce necessary packages that are required for the code to run.
        No need to provide subpackages that will be automatically installed in python {python_version}.
        Don't provide any extra text at the end or front, just write the packages without versions. It will be used for installation.
    """

    text_splitter = PythonCodeTextSplitter(chunk_size=100000, chunk_overlap=0)
    chunks = text_splitter.split_text(file_content)
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
    return final_output, key_index



def merge_packages(package_summary: Dict[str, str], python_version: str = '3.12') -> str:
    """
    Merge and clean multiple sets of Python package requirements using an LLM.

    This function takes a dictionary of raw requirement strings (e.g., from different code modules),
    merges them, and uses an LLM to deduplicate, clean, and filter the list.

    Args:
        package_summary (Dict[str, str]): A dictionary where each value is a string of
                                          package names (one per line).

    Returns:
        str: A cleaned, deduplicated, and minimal list of packages suitable for a requirements file.
    """
    merged_requirements = "\n".join(package_summary.values())

    llm = get_groq_client()

    system_prompt = SystemMessage(content="""
        You are a Python dependency cleaner. Your job is to process raw requirement lists.
        Only return clean, deduplicated, and installable packages.
    """)

    user_prompt = f"""
        Below is a raw list of requirement entries, possibly from multiple sources:

        {merged_requirements}

        Please:
        - Merge and clean the list
        - Remove duplicates
        - Remove any version specifications, just keep package names
        - Ensure all packages are valid Python packages
        - Exclude packages that are standard with Python {python_version}
        - Output only the cleaned list (no explanations, no extra formatting)

        The result will be written directly to a requirements.txt file.
    """

    messages = [system_prompt, HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)

    return response.content.strip()


