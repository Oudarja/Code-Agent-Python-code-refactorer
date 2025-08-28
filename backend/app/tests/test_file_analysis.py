import pytest
from unittest.mock import patch, MagicMock
from services.file_analysis_service import generate_file_analysis

# Sample test inputs
sample_code = """
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('172.16.2.155', 4370))
    print("TCP port is open!")
except:
    print("TCP port is closed or unreachable.")
s.close()
"""

file_path = "network_scan.py"


@patch("services.file_analysis_service.get_groq_client")
def test_generate_file_analysis(mock_get_client):
    
    # Mock the LLM client and its response
    mock_llm = MagicMock()
    
    # Set up the mock to return a fake analysis response every time invoke is called
    mock_llm.invoke.return_value.content = "Mocked analysis result"

    # Assign the mock to the patch
    mock_get_client.return_value = mock_llm

    # Run the function
    result = generate_file_analysis(file_path, sample_code)

    # Assert that the result is as expected
    assert result == "Mocked analysis result"
    assert mock_llm.invoke.call_count >= 1
