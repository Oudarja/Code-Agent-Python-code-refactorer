from groq import Groq
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
MODEL = os.getenv("GROQ_MODEL")
TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
TOP_P = float(os.getenv("GROQ_TOP_P", "0.9"))
MAX_COMPLETION_TOKENS = int(os.getenv("GROQ_MAX_COMPLETION_TOKENS", "120000"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY1 = os.getenv("GROQ_API_KEY1")
GROQ_API_KEY2 = os.getenv("GROQ_API_KEY2")
GROQ_API_KEY3 = os.getenv("GROQ_API_KEY3")
GROQ_API_KEY4 = os.getenv("GROQ_API_KEY4")
GROQ_API_KEY5 = os.getenv("GROQ_API_KEY5")

def get_groq_client(key_index : int = 0) -> Groq:
    """
    Initializes and returns a Groq client instance using the API key from environment variables.

    Returns:
        Groq: An instance of the Groq client.

    Raises:
        ValueError: If the GROQ_API_KEY is missing in the environment.
    """
    api_keys = [GROQ_API_KEY, GROQ_API_KEY1, GROQ_API_KEY2, GROQ_API_KEY3]

    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in environment.")
    else:
        llm = ChatGroq(
        api_key=api_keys[key_index],
        model_name=MODEL,
        streaming=False,
        )
        return llm
