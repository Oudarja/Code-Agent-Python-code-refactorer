"use client";
import React, { useEffect, useState } from "react";
import { extractFiles, extractFileContent } from "@/lib/github_api";
import { useRepo } from "@/context/RepoContext";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function Home() {
  const { owner, repo, branch, files, setFiles } = useRepo();
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (owner && repo && branch) {
      extractFiles(owner, repo, branch)
        .then((data) => setFiles(data))
        .catch((error) => console.error("Error fetching files:", error));
    }
  }, [owner, repo, branch, setFiles]);

  const handleFileClick = async (file) => {
    setSelectedFile(file);
    setFileContent("");
    setLoading(true);

    try {
      const content = await extractFileContent(owner, repo, branch, file);
      setFileContent(content);
    } catch (error) {
      console.error("Error fetching file content:", error);
      setFileContent("Error loading file content.");
    } finally {
      setLoading(false);
    }
  };

  // Detect language from file extension
  const getLanguage = (fileName) => {
    if (!fileName) return "text";
    const ext = fileName.split(".").pop();
    const map = {
      js: "javascript",
      jsx: "javascript",
      ts: "typescript",
      tsx: "typescript",
      py: "python",
      java: "java",
      html: "html",
      css: "css",
      json: "json",
      md: "markdown",
      yml: "yaml",
      yaml: "yaml",
    };
    return map[ext] || "text";
  };

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100 mt-0">
      {/* Owner, Repo, Branch row */}
      <div className="flex flex-wrap gap-6 mb-6 text-lg font-semibold">
        <span>
          Owner: <span className="text-blue-400">{owner}</span>
        </span>
        <span>
          Repo: <span className="text-green-400">{repo}</span>
        </span>
        <span>
          Branch: <span className="text-purple-400">{branch}</span>
        </span>
      </div>

      {/* Total files */}
      <div className="mb-4 text-sm text-gray-300">
        Total Files: <span className="font-bold">{files?.length || 0}</span>
      </div>

      {/* Split layout */}
      <div className="flex gap-4">
        {/* File list */}
        <div className="w-1/3 bg-gray-800 rounded-lg border border-gray-700 p-3 overflow-y-auto max-h-[75vh]">
          <ul className="space-y-2">
            {files?.map((file, index) => {
              const isFolder = file.endsWith("/");
              return (
                <li
                  key={index}
                  onClick={() => !isFolder && handleFileClick(file)}
                  className={`p-2 flex items-center gap-2 rounded-lg transition-colors cursor-pointer hover:bg-gray-700 ${
                    isFolder ? "opacity-70 cursor-not-allowed" : ""
                  } ${selectedFile === file ? "bg-gray-700" : ""}`}
                >
                  <span>{isFolder ? "📁" : "📄"}</span>
                  <span className="truncate">{file}</span>
                </li>
              );
            })}
          </ul>
        </div>

        {/* Code viewer */}
        <div className="flex-1 bg-gray-800 rounded-lg border border-gray-700 p-4 overflow-y-auto max-h-[75vh]">
          {selectedFile ? (
            <>
              <h2 className="mb-3 font-bold text-lg text-blue-300">
                {selectedFile}
              </h2>
              {loading ? (
                <div className="animate-pulse text-gray-400">Loading...</div>
              ) : (
                <SyntaxHighlighter
                  language={getLanguage(selectedFile)}
                  style={vscDarkPlus}
                  wrapLongLines={true}
                  customStyle={{
                    borderRadius: "8px",
                    padding: "16px",
                    fontSize: "14px",
                  }}
                >
                  {fileContent}
                </SyntaxHighlighter>
              )}
            </>
          ) : (
            <div className="text-gray-500 italic">
              Select a file to view its content
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
