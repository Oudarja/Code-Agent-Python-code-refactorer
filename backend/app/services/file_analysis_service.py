import os
import re
import time
from typing import List
from dotenv import load_dotenv
from utils.llm_utils.create_groq_client import get_groq_client
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.text_splitter import PythonCodeTextSplitter
from loguru import logger

def generate_file_analysis(file_path:str, code_content:str) -> str:
    """
    Analyzes a given Python source file using an LLM by chunking its content and passing it through a 
    conversation-based prompt. Returns a detailed analysis of the file including structure, potential 
    improvements, and insights.

    This function simulates a step-by-step interaction with the LLM where:
    - The LLM is first instructed to remember incoming chunks.
    - Each chunk of code is sent sequentially.
    - A final instruction triggers the full analysis.
    - Rate-limiting is handled gracefully with retry logic.

    Args:
        file_path (str): File name of selelcted file like (main.py, utils.py) 
        code_content (str): Content of selected file

    Raises:
        e: If an error other than rate-limiting occurs during communication with the LLM.

    Returns:
        str: Response from LLM 
    """    
    
    llm = get_groq_client()

    # Prompts
    system_prompt = SystemMessage(content="You are a senior Python code reviewer.Your job is to identify issues in Python code chunks.")

    init_prompt = f"""
        I will send you a large file by chunking. File name is : {file_path}. you just read all the chunks also remember issues in code. whenever I will say that all chunks are provided, then you should analyze the full code file. No need to say anything, you can say just next.. ok?
    """

    final_instruction ="""
            You now have the full code.

            Your task:
            "Focus on detecting the following problems:
                - Outdated or deprecated Python syntax
                - Hard-coded values and magic numbers
                - Code smells (long functions, deep nesting, etc.)
                - Common anti-patterns (e.g., mutable default args, bad exception handling)
                - Bad practices affecting readability or maintainability
                Return a concise list of issues found in the code. Do not suggest fixes.
                Do not refactor. Only analyze problems.
                response in markdown format.
            """
    text_splitter = PythonCodeTextSplitter(chunk_size=100000, chunk_overlap=0)
    chunks = text_splitter.split_text(code_content)
    chunks.insert(0, init_prompt)
    chunks.append(final_instruction)

    messages = [system_prompt]
    final_output = ''
    
    for chunk in chunks:
        messages.append(HumanMessage(content=chunk))
        while True:
            try:
                response = llm.invoke(messages) 
                break  # Exit loop on success
            except Exception as e:
                msg = str(e)
                if "rate limit" in msg.lower() or "Rate limit reached" in msg:
                    # Extract retry time from error message
                    wait_match = re.search(r"in (\d+m\d+\.\d+s)", msg)
                    wait_time = 180  # fallback: wait 3 minutes
                    if wait_match:
                        wait_str = wait_match.group(1)
                        minutes = int(wait_str.split("m")[0])
                        seconds = float(wait_str.split("m")[1].replace("s", ""))
                        wait_time = int(minutes * 60 + seconds)
                    logger.info(f"Rate limit hit, waiting {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    raise e

        messages.append(AIMessage(content=response.content))
    return response.content
