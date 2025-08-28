'use client';

import React, { useState } from 'react';
import { useRepo } from '@/context/RepoContext';
import { updateDependencies } from '@/lib/dependency_management_api';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function Home() {
  const { owner, repo, pythonVersion, installedPackages, setInstalledPackages} = useRepo();

  const [loading, setLoading] = useState(false);
  const [responseMsg, setResponseMsg] = useState(''); 

  const handleUpdateDependencies = async () => {
    setLoading(true);
    setResponseMsg('');
    setInstalledPackages();

    try {
      const response = await updateDependencies('temp_refactored_repo', pythonVersion);
      setResponseMsg(response.message || 'No message returned');
      setInstalledPackages(response.installed_packages || '');
      
      
    } catch (error) {
      setResponseMsg(`❌ ${error?.message || 'Unexpected error occurred'}`);
    }

    setLoading(false);
  };

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <h1 className="text-2xl font-bold mb-6">Dependency Management</h1>

      {/* Info Row */}
      <div className="flex flex-wrap items-center gap-6 mb-4 text-lg">
        <p>Owner: <span className="text-blue-400">{owner || '-'}</span></p>
        <p>Repo: <span className="text-green-400">{repo || '-'}</span></p>
        <p>Python Version: <span className="text-yellow-400">{pythonVersion}</span></p>
      </div>

      {/* Button */}
      <div className="flex justify-center mb-6">
        <button
          onClick={handleUpdateDependencies}
          disabled={loading || !owner || !repo}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg disabled:opacity-50"
        >
          {loading ? 'Updating...' : 'Update Dependencies'}
        </button>
      </div>

      {loading && (
        <div>
            <img 
            src="/Loading.gif" 
            alt="Loading..." 
            className="w-16 h-16 rounded-full mx-auto block" 
          />
          <h1 className="text-center text-green-400 mt-4">Dependency validation is in progress... Please wait.!</h1>
        </div>
      )}


      {/* Installed Packages */}
      {installedPackages && (
        
        <div className="mt-6">
          <p className="text-lg font-semibold mb-2">Installed Packages:</p>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 overflow-x-auto">
            <SyntaxHighlighter language="python" style={vscDarkPlus}>
              {installedPackages}
            </SyntaxHighlighter>
          </div>
        </div>
      )}
    </div>
  );
}
