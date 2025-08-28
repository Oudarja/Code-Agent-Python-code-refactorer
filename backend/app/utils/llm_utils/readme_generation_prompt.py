import re
import time
from typing import Dict
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.text_splitter import PythonCodeTextSplitter
from utils.llm_utils.create_groq_client import get_groq_client
from loguru import logger

def file_summary(file_content: str, file_name: str, key_index = 0) -> str:
    """
    Summarizes a Python file by sending its content (in chunks) to the LLM.

    Args:
        file_content: Raw content of the Python file.
        file_name: File name (used for context in summary).

    Returns:
        A summary string describing the file's purpose and behavior.
    """

    llm = get_groq_client(key_index)
    # Prompts
    system_prompt = SystemMessage(content="You are a professional Python code analyst and documentation expert.")

    init_prompt = f"""
        I will send you a large file by chunking. You just read all the chunks and remember the import modules and file name: {file_name}. 
        Whenever I say that all chunks are provided, you should summarize the file and this summary will be used for automatic README generation.
        No need to respond to the earlier chunks; just say 'next..' until I tell you all chunks are provided.
    """

    final_instruction = f"""
        All chunks are provided. Now analyze the full code and produce a summary that explains what `{file_name}` does.
        It should be concise and clear, suitable for inclusion in a README.md. Highlight the core logic, key components, and any noteworthy behavior.
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



def generate_readme_from_repo_summary(repo_summary: Dict[str, str], python_version: str) -> str:
    """
    Generates a structured README.md from file-level summaries and Python version.

    Args:
        repo_summary: Mapping of file paths to their summaries.
        python_version: The Python version used in the project.

    Returns:
        A full README string in markdown format.
    """
    llm = get_groq_client()

    system_prompt = SystemMessage(content="""
        You are a professional technical writer and Python developer. Your job is to generate a clear, structured README.md file 
        for a Python repository based on summarized descriptions of each file and the Python version used.
        Make sure the README includes a project overview, key components, and a 'Getting Started' section.
    """)

    file_summaries = ""
    for file, summary in repo_summary.items():
        file_summaries += f"### `{file}`\n{summary.strip()}\n\n"

    user_prompt = f"""
        Generate a complete README.md using the following context:

        **Python Version:** {python_version}

        **File Summaries:**
        {file_summaries}

        Make sure the README includes:
        - Project Title (use a generic placeholder like "Project Title")
        - Short description of what the project does
        - Python version used
        - Section: Features (based on what the files do)
        - Section: File Descriptions (based on the summaries above)
        - Section: Getting Started (with placeholder installation instructions with new environment setup)
        - Optional: Usage or Example if possible

        Use proper markdown formatting.
    """

    messages = [system_prompt, HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)

    return response.content.strip()
