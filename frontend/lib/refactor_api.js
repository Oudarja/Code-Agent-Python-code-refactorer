const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function refactorRepository(owner, repo, branch, files, python_version) {
  try {
    const response = await fetch(`${baseUrl}/code-agent-api/refactor-python-files`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        owner,
        repo,
        branch,
        files,
        python_version,
        output_dir: "temp_refactored_repo"
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error in refactorRepository:", error);
    throw error;
  }
}
