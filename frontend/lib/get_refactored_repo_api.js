const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function getRefactoredContents() {
  const res = await fetch(`${baseUrl}/code-agent-api/get-refactored-content`);

  if (!res.ok) {
    throw new Error(`Failed to get refactored contents: ${res.status}`);
  }

  const data = await res.json(); // ✅ Parse the JSON body
  console.log("✅ Received from backend:", data);

  // Optional: Validate it's an object
  if (!data.files || typeof data.files !== "object") {
    console.error("❌ Unexpected data format for files:", data.files);
    return {};
  }

  return data.files; // ✅ Return the object with filenames as keys
}
