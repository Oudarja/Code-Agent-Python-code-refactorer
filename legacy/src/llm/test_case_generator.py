

def generate_test_cases(client, python_version,contents, file_name=None):
    """
    Generate unit test cases for a given Python code snippet using the LLM.
    :param client: The LLM client instance.
    :param python_version: The Python version to ensure compatibility.
    :param contents: The Python code snippet to generate tests for.
    :param file_name: Optional name of the file to import functions from.
    :return: Generated test cases as a string.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and test engineer. "
                "Given a Python function, class, or script, generate well-structured unit test cases using the `pytest` framework. "
                "Ensure all important behaviors are covered, and use meaningful test method names.\n\n"
                "Only return raw test code without any explanations or markdown formatting."
            )
        },
        {
            "role": "user",
            "content": (
                f"Generate test cases for the following code:\n\n{contents}"
                f"For importing module or functions, use the file name '{file_name}\n"
                f"Ensure the test cases are compatible with Python {python_version} and follow best practices for `pytest`.\n"
                f"Do not include any explanations, comments, or markdown formatting. It will directly be used for testing."
            )
        }
    ]
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        max_completion_tokens=2048*2
    )
    return response.choices[0].message.content.strip()
