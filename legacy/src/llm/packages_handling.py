import os

def get_packages(client, file_content, python_version):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a dependency manager. You will be given a code snippet and the expected Python version. "
                "Your task is to analyze all imported modules and generate required packages with versions."
                "No need to provide subpackages that will be automatically installed."
            )
        },
        {
            "role": "user",
            "content": (
                f"Expected Python Version: python {python_version}\n\n"
                f"Analyze and produce packages for this code:\n{file_content}\n\n"
                f"you are using always older packages version. but i need latest package version compatible to python{python_version}\n"
                f"Produce packages that can mustly be installed on python{python_version} and must be in pypi.org\n"
                f"You are generating sometimes such version that are not compatible with python{python_version}. use updated version for python{python_version} that are lates packages version"
                f"Please write just the packages (with versions), no explanation. It will be used for installation."
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.1,
        top_p=0.95,
        max_tokens=2048  
    )
    return response.choices[0].message.content.strip()


def merge_packages(client, package_summary, python_version):
    merged_requirements = "\n".join(package_summary.values())
    # return merged_requirements

    messages = [
        {
            "role": "system",
            "content": (
                "You are a dependency manager. You will be given a requirements text. "
                f"Your task is to merge all packages without conflicts for Python {python_version}."
            )
        },
        {
            "role": "user",
            "content": (
                f"Here are the requirements packages:\n{merged_requirements}\n\n"
                f"Merge them and output a clean requirements list (with versions). No explanation."
                f"In case of packages version, use mid label stable version from allpossible version for python{python_version} that will be compatible with python{python_version}"
                f"You know that some packages are inbuilt in pytho {python_version}. You can remove these also.\n"
                f"just return clean requirements file, no additional text. it will be used for installation"
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.1,
        top_p=0.95,
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()


def generate_dependencies(client, root_dir, files_path: list, python_version: str):
    package_summary = {}
    for file_path in files_path:
        if not file_path.endswith(".py") or file_path == "requirements.txt":
            continue
        full_path = os.path.join(root_dir, file_path)
        with open(full_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        packages = get_packages(client, file_content, python_version)
        package_summary[file_path] = packages

    requirements = merge_packages(client, package_summary, python_version)
    return requirements
