const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function codeDiff(old_content, refactored_content) {
  try {
    const payload = {
      old_code: old_content,
      refactored_code: refactored_content,
    };

    // console.log("Payload:", payload);

    const response = await fetch(`${baseUrl}/code-agent-api/get-code-diff`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // console.log(response);

    const data = await response.json();
    // console.log("Parsed JSON:", data);
    return data;
  } catch (error) {
    console.error("Error in codeDiff:", error);
    throw error;
  }
}
