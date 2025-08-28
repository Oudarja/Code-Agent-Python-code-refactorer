# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
def generate_updated_dependencies(client, requirements_text, python_version, code):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Python dependency expert.\n"
                "Your task is to clean and upgrade a requirements.txt file based on the target Python version.\n\n"
                "Instructions:\n"
                "- Upgrade all packages to the latest versions that are compatible with the specified Python version.\n"
                "- Remove sub-packages or libraries that are installed automatically as dependencies (e.g., typing-extensions, six, certifi if not directly used).\n"
                "- Every listed package must be valid and available on PyPI.\n"
                "- All versions must work with the specified Python version.\n"
                "- Return only valid requirements.txt content with exact version pins (e.g., requests==2.31.0).\n"
                "- Do not include explanations, markdown, or any extra text — only one clean package line per line, pip-installable."
            )
        },
        {
            "role": "user",
            "content": (
                f"Target Python version: {python_version}\n\n"
                f"Current requirements.txt:\n{requirements_text}\n\n"
                f"Return the updated list of top-level dependencies only, with latest compatible versions from PyPI that are compatible with python{python_version}.NO explanation,i will use it for installation."
            )
        }
    ]



    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        max_completion_tokens=512*4
    )

    return response.choices[0].message.content.strip()

def fix_broken_dependencies(client, updated_requirements_text, python_version, installation_error, instruction):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Python dependency expert.\n"
                "Fix only the packages in `requirements.txt` that caused installation errors.\n\n"
                "Rules:\n"
                "- Keep all other packages unchanged.\n"
                "- Ensure compatibility with the given Python version.\n"
                "- Only use valid versions from PyPI.\n"
                "- Do not include deprecated packages.\n"
                "- Output a clean `requirements.txt`: one package per line with exact version, no extra text."
            )
        },
        {
            "role": "user",
            "content": (
                f"Python version: {python_version}\n\n"
                f"Requirements:\n{updated_requirements_text}\n\n"
                f"Error log:\n{installation_error}\n\n"
                f"Fix only what's broken. Keep everything else the same.Just return clean requirements file, no additional text, it will be used for installation."
            )
        }
    ]


    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.2,
        top_p=0.9,
        max_completion_tokens=2048
    )

    return response.choices[0].message.content.strip()

# Testing with gemini

# def generate_updated_dependencies(client, requirements_text, python_version, code):
#     # Load API key from .env
#     load_dotenv()
#     api_key = os.getenv("GEMINI_API_KEY")

#     if not api_key:
#         raise ValueError("GEMINI_API_KEY not found in .env file")

#     # Configure Gemini
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel("gemini-1.5-pro")

#     # Prompt parts
#     prompt = [
#         "You are a professional Python dependency and environment manager with full knowledge of PyPI compatibility across Python versions.\n"
#         "Your task is to update the given requirements.txt to ensure:\n"
#         "1. All listed packages are actually used in the provided Python code (based on import analysis).\n"
#         "2. All package versions are valid and available on PyPI.\n"
#         "3. All packages with version are compatible with the target Python version. Follow it strictly, as we're facing version issues.\n"
#         "4. The generated list avoids all known version conflicts and installation errors (like conflicting requirements between packages).\n"
#         "5. Remove any deprecated or removed libraries (e.g., `distutils`, `unittest`, `Queue`, etc.).\n"
#         "6. You MUST resolve any version conflicts between interdependent packages, e.g., pytest and pluggy.\n"
#         "7. Don't provide any version that actually does not exist. Be careful about version validity.\n"
#         "Return ONLY the updated requirements.txt with exact version numbers — one valid line per package, no explanations, markdown, or comments."
#     ]

#     prompt.append(f"Target Python version: {python_version}")
#     prompt.append(f"Current requirements.txt:\n{requirements_text}")
#     prompt.append(f"Python code to analyze:\n{code}")
#     prompt.append("Return only the compatible and installable requirements.txt content (no explanations).")

#     # Call Gemini
#     response = model.generate_content(prompt)

#     return response.text.strip()
