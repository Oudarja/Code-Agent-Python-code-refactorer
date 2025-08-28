const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
export async function generateReadme(root_dir, python_version) {

  const res = await fetch(
    `${baseUrl}/code-agent-api/generate-readme?root_dir=${encodeURIComponent(root_dir)}&python_version=${encodeURIComponent(python_version)}`
  );

  if (!res.ok) {
    throw new Error(`Failed to generate readme: ${res.status}`);
  }

  return await res.json();
}