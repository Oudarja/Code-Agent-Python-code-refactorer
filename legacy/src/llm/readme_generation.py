# Readme generation process
import os
def file_summary(client, file_path, file_content, python_version):
    """
    Summarizes a single Python file's purpose and functionality for use in repository documentation.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a professional Python code analyst and documentation expert. "
                f"Your task is to generate a concise and clear natural language summary of the purpose and functionality "
                f"of the given Python file. The summary will be used for auto-generating documentation such as README files."
            )
        },
        {
            "role": "user",
            "content": (
                f"File Path: {file_path}\n"
                f"Python Version: {python_version}\n\n"
                f"Code:\n{file_content}\n\n"
                f"Please provide a short summary (3 to 6 sentences) that explains what this file does."
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.1,
        top_p=0.9,
        max_completion_tokens=512 * 4
    )

    return response.choices[0].message.content.strip()


def generate_repo_summary(client, root_dir, files_path: list, python_version):
    repo_summary = {}
    for file_path in files_path:
        # read file content
        full_path = os.path.join(root_dir, file_path)
        with open(full_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        repo_summary[file_path] = file_summary(client, file_path, file_content, python_version)
    return repo_summary

def generate_readme(client, root_dir, files_path: list, python_version):
    """
    Generates a high-quality README.md for the full repository.
    Includes setup instructions, virtual environment steps, usage, and file structure.
    """
    repo_summary = generate_repo_summary(client, root_dir, files_path, python_version)

    formatted_summaries = "\n\n".join(
        f"### `{path}`\n{summary}" for path, summary in repo_summary.items()
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional software engineer and expert technical writer. "
                "You help developers create high-quality, production-ready `README.md` files for Python projects."
            )
        },
        {
            "role": "user",
            "content": (
                f"The repository uses Python {python_version} and contains the following file summaries:\n\n"
                f"{formatted_summaries}\n\n"
                f"Using the above summaries, generate a detailed `README.md` that includes:\n"
                f"- A professional project title\n"
                f"- A short, clear description of the project\n"
                f"- Step-by-step setup instructions including:\n"
                f"  - How to create a virtual environment using `venv`\n"
                f"  - How to activate it (for Windows/macOS/Linux)\n"
                f"  - How to install dependencies from `requirements.txt`\n"
                f"- How to run the project (e.g., `python main.py` or similar)\n"
                f"- Example usage if applicable\n"
                f"- An overview of the file structure\n"
                f"- (Optional) Contribution guidelines or license section\n\n"
                f"Use proper Markdown formatting for all sections and ensure the tone is helpful and developer-friendly."
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.1,
        top_p=0.9,
        max_completion_tokens=512 * 4
    )

    return response.choices[0].message.content.strip()
