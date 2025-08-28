const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
export async function extractOwnerRepo(repoUrl) {

  const res = await fetch(
    `${baseUrl}/code-agent-api/extract-owner-repo?repo_url=${encodeURIComponent(repoUrl)}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch owner/repo: ${res.status}`);
  }

  return await res.json();
}

export async function fetchBranches(owner, repo) {
  const res = await fetch(
    `${baseUrl}/code-agent-api/extract-branch?owner=${encodeURIComponent(owner)}&repo=${encodeURIComponent(repo)}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch branches: ${res.status}`);
  }

  return await res.json();
}

export async function extractFiles(owner, repo, branch) {
  const res = await fetch(
    `${baseUrl}/code-agent-api/extract-files?owner=${encodeURIComponent(owner)}&repo=${encodeURIComponent(repo)}&branch=${encodeURIComponent(branch)}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch files: ${res.status}`);
  }

  return await res.json();
}

export async function extractFileContent(owner, repo, branch, filePath) {
  const res = await fetch(
    `${baseUrl}/code-agent-api/get-github-file-content?owner=${encodeURIComponent(owner)}&repo=${encodeURIComponent(repo)}&file_path=${encodeURIComponent(filePath)}&branch=${encodeURIComponent(branch)}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch file content: ${res.status}`);
  }

  return await res.json();
}


// This function commits and pushes changes to the repository 

export async function commitPushRepository(owner, repo, commit_message, branch_name) {
  try {
    const response = await fetch(`${baseUrl}/code-agent-api/commit-push`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        owner,
        repo,
        commit_message,
        branch : branch_name,
        base_branch : 'main'
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Handle the response if it returns a simple message
    const data = await response.json();
    if (data && data.message) {
      console.log("Success:", data.message);
      return data.message;  // You can return the message or handle it as needed
    }

    // If the response doesn't include a 'message' field, log the entire response
    console.log("Response:", data);
    return data;
  } catch (error) {
    console.error("Error in commitPushRepository:", error);
    throw error;  // Throw the error to be handled by the caller
  }
}


//  This function creates a pull request on GitHub
export async function createGitPR(owner, repo, src_branch, dest_branch, title, body) {
  try {
    const response = await fetch(`${baseUrl}/code-agent-api/git-pr`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        owner,
        repo,
        head_branch : src_branch,
        base_branch : dest_branch,
        title,
        body,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    // Check for success and log the appropriate message
    if (data.success) {
      const successMessage = `PR created: ${data.url}`;
      console.log("Success:", successMessage);
      return successMessage;
    } else {
      console.error("Failed to create PR:", data.message);
      return data.message;
    }
  } catch (error) {
    console.error("Error in createGitPR:", error);
    throw error;
  }
}
