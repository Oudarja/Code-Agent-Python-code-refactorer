const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function fileAnalyzer(file_path, code_content) {
  try {
    const response = await fetch(
      `${baseUrl}/code-agent-api/get-file-analysis`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          file_path,
          code_content,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error in refactorRepository:", error);
    throw error;
  }
}
