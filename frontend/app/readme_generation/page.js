'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useRepo } from '@/context/RepoContext';
import { generateReadme } from '@/lib/readme_generation_api';
import { getRefactoredContents } from '@/lib/get_refactored_repo_api';
import ReactMarkdown from 'react-markdown';

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function Home() {
  const {
    owner,
    repo,
    pythonVersion,
    refactoredRepoContents,
    setRefactoredRepoContents
  } = useRepo();

  const [loading, setLoading] = useState(false);
  const [responseMsg, setResponseMsg] = useState('');
  const [readmeContent, setReadmeContent] = useState('');

  // Fetch README.md from refactored repo contents
  const fetchRefactoredContents = useCallback(async () => {
    try {
      const refactoredContents = await getRefactoredContents(); // returns the 'files' object directly
      setRefactoredRepoContents(refactoredContents || { 'abc.py': 'print("Hello World")' });
      setReadmeContent(refactoredContents?.['README.md'] || '');
    } catch (error) {
      console.error('Error fetching refactored contents:', error);
      setRefactoredRepoContents({ 'abc.py': 'print("Hello World")' });
      setReadmeContent('');
    }
  }, [setRefactoredRepoContents]);

  useEffect(() => {
    fetchRefactoredContents();
  }, [fetchRefactoredContents]);

  const handleGenerateReadme = async () => {
    setLoading(true);
    setResponseMsg('');

    try {
      const response = await generateReadme('temp_refactored_repo', pythonVersion);
      setResponseMsg(response?.message || '✅ README.md generated successfully.');
      await fetchRefactoredContents(); // Refresh content after generation
    } catch (error) {
      setResponseMsg(`❌ ${error?.message || 'Unexpected error occurred'}`);
    }

    setLoading(false);
  };

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <h1 className="text-2xl font-bold mb-6">Generate README.md</h1>

      {/* Info Row */}
      <div className="flex flex-wrap items-center gap-6 mb-4 text-lg">
        <p>Owner: <span className="text-blue-400">{owner || '-'}</span></p>
        <p>Repo: <span className="text-green-400">{repo || '-'}</span></p>
        <p>Python Version: <span className="text-yellow-400">{pythonVersion}</span></p>
      </div>

      {/* Button */}
      <div className="flex justify-center mb-6">
        <button
          onClick={handleGenerateReadme}
          disabled={loading || !owner || !repo}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate README'}
        </button>
      </div>

      {loading && (
        <div>
            <img 
            src="/Loading.gif" 
            alt="Loading..." 
            className="w-16 h-16 rounded-full mx-auto block" 
          />
          <h1 className="text-center text-green-400 mt-4">Readme generation is in progress... Please wait.!</h1>
        </div>
      )}

      {/* Response Message */}
      {responseMsg && (
        <div className="mt-6 text-center text-base font-medium text-white bg-gray-800 px-4 py-3 rounded border border-gray-700">
          {responseMsg}
        </div>
      )}

      {/* Render README.md */}
      {readmeContent ? (
        <div className="mt-8">
          <p className="text-lg font-semibold mb-2">README.md Content:</p>
          <div className="prose prose-invert max-w-none bg-gray-800 p-6 rounded-lg border border-gray-700 overflow-x-auto">
            <SyntaxHighlighter
                language={'markdown'}
                style={vscDarkPlus}
                wrapLongLines={true}
                customStyle={{
                  borderRadius: '8px',
                  padding: '16px',
                  fontSize: '14px',
                }}
              >
                {readmeContent}
            </SyntaxHighlighter>
          </div>
        </div>
      ) : (
        <div className="mt-8 text-sm text-gray-400 italic">
          No README.md found in the refactored repository.
        </div>
      )}
    </div>
  );
}
