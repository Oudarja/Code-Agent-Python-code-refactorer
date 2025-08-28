"use client";

import React, { useEffect, useState } from "react";
import { extractFiles, extractFileContent } from "@/lib/github_api";
import { fileAnalyzer } from "@/lib/file_analysis_api";
import { codeDiff } from "@/lib/file_change_api.js";
import { useRepo } from "@/context/RepoContext";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const { owner, repo, branch, files, setFiles, refactoredRepoContents } =
    useRepo();
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileChange, setFileChange] = useState("");

  useEffect(() => {
    if (owner && repo && branch) {
      extractFiles(owner, repo, branch)
        .then((data) => setFiles(data))
        .catch((error) => console.error("Error fetching files:", error));
    }
  }, [owner, repo, branch, setFiles]);

  useEffect(() => {
    if (fileContent && selectedFile && refactoredRepoContents[selectedFile]) {
      codeDiff(fileContent, refactoredRepoContents[selectedFile])
        .then((data) => setFileChange(data))
        .catch((error) => console.log("Error fetching files", error));
    }
  }, [fileContent, selectedFile, refactoredRepoContents]);

  const handleFileChange = async (e) => {
    const file = e.target.value;
    setSelectedFile(file);
    setFileContent("");
    setAnalysis("");
    setLoading(true);

    try {
      const content = await extractFileContent(owner, repo, branch, file);
      setFileContent(content);

      const result = await fileAnalyzer(file, content);
      setAnalysis(result || "No analysis available.");
    } catch (error) {
      console.error("Error fetching file or analysis:", error);
      setFileContent("Error loading file content.");
      setAnalysis("Error loading AI analysis.");
    } finally {
      setLoading(false);
    }
  };

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
      {/* File dropdown */}
      <div className="mb-6">
        <label className="block mb-2 text-sm font-semibold text-gray-300">
          Select File:
        </label>
        <select
          onChange={handleFileChange}
          value={selectedFile || ""}
          className="w-full bg-gray-800 text-gray-100 border border-gray-600 rounded px-3 py-2 focus:outline-none"
        >
          <option value="" disabled>
            -- Choose a file --
          </option>
          {files?.map((file, index) =>
            file.endsWith("/") ? null : (
              <option key={index} value={file}>
                {file}
              </option>
            )
          )}
        </select>
      </div>

      {/* Code + Analysis viewer */}
      <div className="flex gap-4">
        {/* Code Viewer */}
        <div className="w-1/2 bg-gray-800 rounded-lg border border-gray-700 p-4 max-h-[75vh]">
          {selectedFile ? (
            <>
              <h2 className="mb-3 font-bold text-lg text-blue-300">
                {selectedFile}
              </h2>
              {loading ? (
                <div className="animate-pulse text-gray-400">Loading...</div>
              ) : (
                <div className="overflow-y-auto max-h-[75vh]">
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
                </div>
              )}
            </>
          ) : (
            <div className="text-gray-500 italic">
              Select a file to view its content
            </div>
          )}
        </div>

        {/* AI Analysis Viewer */}
        <div className="w-1/2 bg-gray-800 rounded-lg border border-gray-700 p-4 max-h-[75vh]">
          {selectedFile ? (
            <>
              <h2 className="mb-3 font-bold text-lg text-purple-300">
                AI analysis
              </h2>
              {loading ? (
                <div className="animate-pulse text-gray-400">Loading...</div>
              ) : (
                <div className="overflow-y-auto max-h-[75vh]">
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
                    {analysis}
                  </SyntaxHighlighter>
                </div>
              )}
            </>
          ) : (
            <div className="text-gray-500 italic">
              Select a file to view its content
            </div>
          )}
        </div>
      </div>

      <div className="flex gap-4 mt-20">
        {/* Refactored code content */}
        <div className="w-1/2 bg-gray-800 rounded-lg border border-gray-700 p-4 max-h-[75vh]">
          {selectedFile ? (
            <>
              <h2 className="mb-3 font-bold text-lg text-green-300">
                Refactored Content
              </h2>
              {loading ? (
                <div className="animate-pulse text-gray-400">Loading...</div>
              ) : (
                <div className="overflow-y-auto max-h-[75vh]">
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
                    {refactoredRepoContents[selectedFile]}
                  </SyntaxHighlighter>
                </div>
              )}
            </>
          ) : (
            <div className="text-gray-500 italic">
              Select a file to view its content
            </div>
          )}
        </div>

        {/* Code diff */}
        <div className="w-1/2 bg-gray-800 rounded-lg border border-gray-700 p-4 max-h-[75vh]">
          <h2 className="mb-3 font-bold text-lg text-yellow-300">Code Diff</h2>
          {selectedFile ? (
            <>
              {loading ? (
                <div className="animate-pulse text-gray-400">Loading...</div>
              ) : (
                <div className="overflow-y-auto max-h-[75vh]">
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
                    {fileChange}
                  </SyntaxHighlighter>
                </div>
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
