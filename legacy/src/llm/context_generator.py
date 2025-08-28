import os
from src.utils.github_utils import get_repo_files, download_file

def summarize_file_with_llm(client, file_path, file_content):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a code summarizer. You will be given a source code file. "
                "Your task is to summarize its purpose and key functionality in concise sentences."
                "You can store information like:"
                "- all imported module must be stored"
                "- metadata on function or classes for provided files."
            )
        },
        {
            "role": "user",
            "content": (
                f"File Path: {file_path}\n\n"
                f"File Content:\n{file_content}\n\n"
                f"Summarize it concisely without repeating code."
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.3,
        top_p=0.95,
        max_tokens=512
    )
    return response.choices[0].message.content.strip()


def generate_context(client, owner, repo, branch):
    all_files = get_repo_files(owner, repo, branch)
    file_summaries = {}
    files_path = []

    for file_path in all_files:
        file_ext = os.path.splitext(file_path)[1]

        # Only summarize readable files
        if file_ext not in [".py", ".md", ".txt", ".json", ".yaml", ".yml"]:
            continue

        try:
            content = download_file(owner, repo, file_path, branch)
            if not content.strip():
                continue

            summary = summarize_file_with_llm(client, file_path, content)
            file_summaries[file_path] = summary
            files_path.append(file_path)

        except Exception as e:
            print(f"[!] Skipped {file_path} due to error: {e}")

    # Join summaries in the desired format
    full_context = "\n".join([f"### {path} ###\n{summary}" for path, summary in file_summaries.items()])
    return full_context