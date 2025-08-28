"""Refactored Streamlit UI for CodeAgent
Features are isolated in separate tabs, expensive operations cached in session_state, and
callbacks are used to avoid full‑page reruns.
All original function names and import paths are preserved.
"""
import os
import shutil
import sys
from pathlib import Path

import streamlit as st
from streamlit_ace import st_ace

# ────────────────────────────────────────────────────────────────────────────────
# PATH SETUP
# ────────────────────────────────────────────────────────────────────────────────
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# ────────────────────────────────────────────────────────────────────────────────
# ORIGINAL IMPORTS (UNCHANGED PATHS & NAMES)
# ────────────────────────────────────────────────────────────────────────────────
from src.utils.github_utils import (
    get_repo_files,
    download_file,
    commit_file,
    create_pull_request,
    get_all_branches,
)
from src.llm.groq_client import get_groq_client
from src.llm.analyzer import analyze_large_code
from src.llm.code_diff import generate_full_diff
from src.llm.update_dependencies import fix_broken_dependencies
from src.llm.requirements_validation import setup_virtualenv_and_install_requirements
from src.utils.refactor_all_files import refactor_all_python_files_in_repo  # ← kept original path
from src.llm.readme_generation import generate_readme
from src.llm.context_generator import generate_context
from src.llm.test_case_generator import generate_test_cases
from src.llm.packages_handling import generate_dependencies

# ────────────────────────────────────────────────────────────────────────────────
# CONSTANTS & INITIAL SESSION STATE
# ────────────────────────────────────────────────────────────────────────────────
DEFAULT_TEMP_DIR = "C:/Cloudly/my_refactored_repo"

st.set_page_config(page_title="CodeAgent UI", layout="wide")

# Initialize once
if "init" not in st.session_state:
    st.session_state.update(
        {
            "init": True,
            "python_version": "3.12",
            "temp_dir": DEFAULT_TEMP_DIR,
            "repo_info": {},  # owner, repo, branches
            "files": [],
            # caches
            "repo_files_cache": {},
            "analysis_cache": {},
        }
    )

# ────────────────────────────────────────────────────────────────────────────────
# SIDEBAR – GLOBAL SETUP
# ────────────────────────────────────────────────────────────────────────────────
sidebar = st.sidebar
sidebar.header("Setup")

python_versions = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]
st.session_state.python_version = sidebar.selectbox(
    "Target Python Version",
    python_versions,
    index=python_versions.index(st.session_state.python_version),
)

repo_url = sidebar.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")

# Validate URL only when it changes
if repo_url and repo_url != st.session_state.repo_info.get("url"):
    parts = repo_url.strip("/").split("/")
    if len(parts) >= 3 and "github.com" in repo_url:
        owner, repo = parts[-2], parts[-1]
        branches, err = get_all_branches(owner, repo)
        st.session_state.repo_info = {
            "url": repo_url,
            "owner": owner,
            "repo": repo,
            "branches": branches or [],
            "error": err or "",
        }
    else:
        st.session_state.repo_info = {"url": repo_url, "error": "❌ Invalid GitHub URL"}

if (err := st.session_state.repo_info.get("error")):
    st.error(err)
    st.stop()

branch = sidebar.selectbox(
    "Branch", st.session_state.repo_info.get("branches", []), key="branch_select"
)

# Singleton Groq client
@st.cache_resource(show_spinner=False)
def _client():
    return get_groq_client()

client = _client()

# ────────────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────────

def get_repo_files_cached(owner: str, repo: str, branch: str):
    key = (owner, repo, branch)
    if key not in st.session_state.repo_files_cache:
        st.session_state.repo_files_cache[key] = get_repo_files(owner, repo, branch)
    return st.session_state.repo_files_cache[key]


def reset_temp_dir():
    tmp = Path(st.session_state.temp_dir)
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    return str(tmp)

# ────────────────────────────────────────────────────────────────────────────────
# TAB LAYOUT – ISOLATED FEATURES
# ────────────────────────────────────────────────────────────────────────────────
TABS = (
    "Overview",
    "Full Refactor",
    "File Analysis / Edit",
    "Dependencies",
    "Documentation",
    "GitHub Push / PR",
)

overview_tab, refactor_tab, file_tab, deps_tab, docs_tab, git_tab = st.tabs(TABS)

# ────────────────────────────────────────────────────────────────────────────────
# 1. OVERVIEW TAB
# ────────────────────────────────────────────────────────────────────────────────
with overview_tab:
    st.header("Repository Overview")
    if repo_url:
        files = get_repo_files_cached(
            st.session_state.repo_info["owner"],
            st.session_state.repo_info["repo"],
            branch,
        )
        st.session_state.files = files
        st.write(f"**{len(files)}** files found in branch `{branch}`")
        st.code("\n".join(files[:50]), language="text")
    else:
        st.info("Enter a repository URL to load files.")

# ────────────────────────────────────────────────────────────────────────────────
# 2. FULL REFACTOR TAB
# ────────────────────────────────────────────────────────────────────────────────
with refactor_tab:
    st.header("Full Repository Refactor")
    if st.button("Refactor Repository", key="btn_refactor_repo"):
        reset_temp_dir()
        with st.spinner("Refactoring…"):
            success, _, log = refactor_all_python_files_in_repo(
                client,
                st.session_state.repo_info["owner"],
                st.session_state.repo_info["repo"],
                branch,
                st.session_state.python_version,
                st,
                st.session_state.temp_dir,
                None,
            )
        st.session_state.refactor_success = success
        st.write(log)
        st.success("Refactor done." if success else "Refactor failed.")

# ────────────────────────────────────────────────────────────────────────────────
# 3. FILE ANALYSIS / EDIT TAB
# ────────────────────────────────────────────────────────────────────────────────
with file_tab:
    st.header("File Analysis & Editing")
    if not st.session_state.files:
        st.info("Load a repository first.")
        st.stop()

    sel_file = st.selectbox("Choose a file", st.session_state.files, key="sel_file")

    # Load original & analysis only if cache miss or button pressed
    if st.button("Load / Refresh Analysis", key="btn_load_analysis") or sel_file not in st.session_state.analysis_cache:
        orig = download_file(
            st.session_state.repo_info["owner"],
            st.session_state.repo_info["repo"],
            sel_file,
            branch,
        )
        analysis = analyze_large_code(client, orig, st)
        st.session_state.analysis_cache[sel_file] = (orig, analysis)
    orig_code, analysis = st.session_state.analysis_cache[sel_file]

    ocol, acol = st.columns(2)
    with ocol:
        st.subheader("Original Code")
        st.code(orig_code, language="python")
    with acol:
        st.subheader("AI Analysis")
        st.markdown(analysis)

    # Editable refactored code
    upd_path = Path(st.session_state.temp_dir) / sel_file
    if upd_path.exists():
        upd_code = upd_path.read_text(encoding="utf-8")
        st.subheader("Refactored Code (editable)")
        edited = st_ace(value=upd_code, language="python", theme="monokai")
        if edited != upd_code:
            upd_path.parent.mkdir(parents=True, exist_ok=True)
            upd_path.write_text(edited, encoding="utf-8")
            st.success("File saved.")
        diff = generate_full_diff(orig_code, edited)
        st.subheader("Diff")
        st.code(diff, language="diff")
        # Test generation
        if "tests" not in sel_file and not sel_file.startswith("test_"):
            if st.button("Generate Unit Tests", key="btn_tests"):
                with st.spinner("Generating tests…"):
                    tests = generate_test_cases(
                        client,
                        st.session_state.python_version,
                        edited,
                        sel_file,
                    )
                tdir = Path(st.session_state.temp_dir) / "tests"
                tdir.mkdir(parents=True, exist_ok=True)
                tfile = tdir / f"test_{Path(sel_file).name}"
                tfile.write_text(tests, encoding="utf-8")
                st.success(f"Tests written to {tfile.relative_to(st.session_state.temp_dir)}")
                st.code(tests, language="python")
    else:
        st.info("Run the full refactor first to create editable files.")

# ────────────────────────────────────────────────────────────────────────────────
# 4. DEPENDENCIES TAB
# ────────────────────────────────────────────────────────────────────────────────
with deps_tab:
    st.header("Dependencies Management")
    req_path = Path(st.session_state.temp_dir) / "requirements.txt"

    if st.button("Generate requirements.txt", key="btn_gen_req"):
        with st.spinner("Generating dependencies…"):
            req_text = generate_dependencies(
                client,
                st.session_state.temp_dir,
                st.session_state.files,
                st.session_state.python_version,
            )
        req_path.write_text(req_text, encoding="utf-8")
        st.success("requirements.txt generated")

    if req_path.exists():
        st.subheader("requirements.txt")
        contents = req_path.read_text(encoding="utf-8")
        edited = st_ace(value=contents, language="text", theme="monokai")
        if edited != contents:
            req_path.write_text(edited, encoding="utf-8")
            st.success("requirements.txt updated")

        if st.button("Validate Dependencies", key="btn_validate"):
            with st.spinner("Validating…"):
                valid, msg, pkgs = setup_virtualenv_and_install_requirements(
                    requirements_text=edited,
                    python_version=st.session_state.python_version,
                )
            if valid:
                st.success("All packages installed")
                st.code("\n".join(pkgs), language="text")
            else:
                st.error("Installation failed")
                st.code(msg, language="text")
                if st.button("Auto‑fix", key="btn_fix"):
                    fixed = fix_broken_dependencies(
                        client,
                        edited,
                        st.session_state.python_version,
                        msg,
                        "Modify dependencies resolving provided error. Return just packages.",
                    )
                    req_path.write_text(fixed, encoding="utf-8")
                    st.success("requirements.txt fixed – re‑validate")
    else:
        st.info("Generate requirements.txt first")

# ────────────────────────────────────────────────────────────────────────────────
# 5. DOCUMENTATION TAB
# ────────────────────────────────────────────────────────────────────────────────
with docs_tab:
    st.header("README generation")
    readme_path = Path(st.session_state.temp_dir) / "README.md"

    if st.button("Generate README", key="btn_readme"):
        with st.spinner("Creating README…"):
            md = generate_readme(
                client,
                st.session_state.temp_dir,
                st.session_state.files,
                st.session_state.python_version,
            )
        readme_path.write_text(md, encoding="utf-8")
        st.success("README.md created")

    if readme_path.exists():
        st.markdown(readme_path.read_text(encoding="utf-8"))

# ────────────────────────────────────────────────────────────────────────────────
# 6. GITHUB PUSH / PR TAB
# ────────────────────────────────────────────────────────────────────────────────
with git_tab:
    st.header("Push & Pull Request")
    if not Path(st.session_state.temp_dir).exists():
        st.info("Nothing to push – run refactor first")
        st.stop()

    new_branch_toggle = st.toggle("Use new branch", True, key="toggle_branch")
    if new_branch_toggle:
        target_branch = st.text_input("Branch name", "refactored-branch", key="inp_branch")
    else:
        target_branch = st.selectbox(
            "Existing branch", st.session_state.repo_info.get("branches", []), key="sel_existing_branch"
        )

    commit_msg = st.text_input("Commit message", "Refactored code via CodeAgent", key="commit_msg")

    if st.button("Push", key="btn_push"):
        with st.spinner("Pushing …"):
            try:
                for p in Path(st.session_state.temp_dir).rglob("*.py"):
                    rel = p.relative_to(st.session_state.temp_dir).as_posix()
                    commit_file(
                        st.session_state.repo_info["owner"],
                        st.session_state.repo_info["repo"],
                        rel,
                        p.read_text(encoding="utf-8"),
                        commit_msg,
                        target_branch,
                    )
                st.success("Push complete")
                st.session_state.last_push = target_branch
            except Exception as e:
                st.error(f"Push failed: {e}")

    if "last_push" in st.session_state:
        dest_branch = st.selectbox(
            "Create PR to", [b for b in st.session_state.repo_info["branches"] if b != st.session_state.last_push], key="dest_branch"
        )
        pr_title = st.text_input("PR title", "Auto Refactor by CodeAgent", key="pr_title")
        pr_body = st.text_area(
            "PR description",
            "This PR contains refactored code and/or updated dependencies generated by CodeAgent.",
            key="pr_body",
        )
        if st.button("Create PR", key="btn_create_pr"):
            with st.spinner("Creating PR..."):
                try:
                    pr_result = create_pull_request(
                        owner=st.session_state.repo_info["owner"],
                        repo=st.session_state.repo_info["repo"],
                        head_branch=st.session_state.last_push,
                        base_branch=dest_branch,
                        title=pr_title,
                        body=pr_body,
                    )
                    if pr_result["success"]:
                        st.success(pr_result["message"])
                        st.markdown(f"[🔗 View PR]({pr_result['url']})", unsafe_allow_html=True)
                    else:
                        st.warning(pr_result["message"])
                except Exception as e:
                    st.error(f"Failed to create PR: {e}")

