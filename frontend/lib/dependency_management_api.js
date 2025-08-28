const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function updateDependencies(root_dir = "temp_refactored_repo", python_version = "3.12") {
  try {
    const response = await fetch(`${baseUrl}/code-agent-api/update-dependencies`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        root_dir: root_dir,
        python_version: python_version
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error in updating dependencies :", error);
    throw error;
  }
}
