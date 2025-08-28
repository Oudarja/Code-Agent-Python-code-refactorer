"use client";
import React, { useEffect, useState } from "react";
import { useRepo } from "@/context/RepoContext";
import { refactorRepository } from "@/lib/refactor_api";
import { getRefactoredContents } from "@/lib/get_refactored_repo_api"; 
 
export default function Home() {
  const {
    owner,
    repo,
    branch,
    files,
    pythonVersion,
    refactoredRepoContents,
    setRefactoredRepoContents,
    logs,
    setLogs,
  } = useRepo();
  const [loading, setLoading] = useState(false);
  const [outputDir, setOutputDir] = useState("");
  const [success, setSuccess] = useState(null);

  const handleRefactor = async () => {
    setLoading(true);
    setLogs([]);
    setSuccess(null);
    try {
      const res = await refactorRepository(
        owner,
        repo,
        branch,
        files,
        pythonVersion
      );
      setSuccess(res.success);
      setOutputDir(res.output_dir || "temp_refactored_repo");
      setLogs(res.logs || []);
    } catch (error) {
      console.error("Error calling refactor API:", error);
      setSuccess(false);
    } finally {
      setLoading(false);
    }
  };
    // Fetch refactored contents after successful refactor
    // try {
    //   const refactoredContents = await getRefactoredContents();
    //   setRefactoredRepoContents(
    //     refactoredContents || { "abc.py": 'print("Hello World")' }
    //   );
    //   console.log("Refactored Contents:", refactoredContents);
    // } catch (error) {
    //   console.error("Error fetching refactored contents:", error);
    //   setRefactoredRepoContents({ "abc.py": 'print("Hello World")' });
    // }

    useEffect(() => {
      const fetchRefactoredContents = async () => {
        try {
          const refactoredContents = await getRefactoredContents();
          setRefactoredRepoContents(
            refactoredContents || { "abc.py": 'print("Hello World")' }
          );
          console.log("Refactored Contents:", refactoredContents);
        } catch (error) {
          console.error("Error fetching refactored contents:", error);
          setRefactoredRepoContents({ "abc.py": 'print("Hello World")' });
        }
      }
      fetchRefactoredContents();
    }, [setRefactoredRepoContents]);



  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <h1 className="text-2xl font-bold mb-6">Full Repository Refactor</h1>

      {/* Repo Info in horizontal row */}
      <div className="flex flex-wrap items-center gap-6 mb-4 text-lg">
        <p>
          Owner: <span className="text-blue-400">{owner}</span>
        </p>
        <p>
          Repo: <span className="text-green-400">{repo}</span>
        </p>
        <p>
          Branch: <span className="text-purple-400">{branch}</span>
        </p>
        <p>
          Python Version:{" "}
          <span className="text-yellow-400">{pythonVersion}</span>
        </p>
      </div>

      {/* Refactor Button in next line, centered */}
      <div className="flex justify-center mb-6">
        <button
          onClick={handleRefactor}
          disabled={loading || files.length === 0 || !owner || !repo || !branch}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg disabled:opacity-50"
        >
          {loading ? "Refactoring..." : "Refactor Repository"}
        </button>
      </div>

      {loading && (
        <div>
            <img 
            src="/Loading.gif" 
            alt="Loading..." 
            className="w-16 h-16 rounded-full mx-auto block" 
          />
          <h1 className="text-center text-green-400 mt-4">Refactoring in progress... Please wait.!</h1>
        </div>
      )}
      
      {/* Success/Failure Message */}
      {success !== null && (
        <div
          className={`mt-4 font-semibold ${
            success ? "text-green-400" : "text-red-400"
          }`}
        >
          {success
            ? "✅ Refactoring completed successfully"
            : "❌ Refactoring failed"}
        </div>
      )}

      {/* Output Directory */}
      {outputDir && !loading &&(
        <div className="mt-6">
          <p className="text-sm text-gray-400">Output Directory:</p>
          <p className="text-yellow-400 font-mono">{outputDir}</p>
        </div>
      )}

      {/* Logs */}
      {logs.length > 0 && (
        <div className="mt-6">
          <p className="text-lg font-semibold mb-2">Refactored Files:</p>
          <ul className="bg-gray-800 rounded-lg p-4 border border-gray-700 space-y-1">
            {logs.map((file, idx) => (
              <li key={idx} className="text-sm text-gray-200">
                📄 {file}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
