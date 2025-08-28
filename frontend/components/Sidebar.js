'use client';
import React, { useEffect, useState } from 'react';
import { extractOwnerRepo, fetchBranches } from '@/lib/github_api';
import { useRepo } from '@/context/RepoContext';

export default function Sidebar({ sidebarOpen, setSidebarOpen }) {
  const {
    pythonVersion, setPythonVersion,
    repoUrl, setRepoUrl,
    owner, setOwner,
    repo, setRepo,
    branch, setBranch,
    branches, setBranches
  } = useRepo();


  const handleFetch = async (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      try {
        const { owner, repo } = await extractOwnerRepo(repoUrl);
        setOwner(owner);
        setRepo(repo);

        const branchList = await fetchBranches(owner, repo);
        setBranches(branchList || []);
        setBranch(branchList[0] || 'main'); // Set default branch to first in list
      } catch (error) {
        console.error("Fetch error:", error);
        alert("Failed to fetch branches. Please check the repository URL.");
      }
    }
  };

  return (
    <div className={`fixed top-0 left-0 h-full w-80 bg-gray-900 text-white shadow-lg z-50 transition-transform duration-300 ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}>
      <div className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Settings</h2>
          <button
            className="px-3 py-1 bg-gray-800 text-white rounded-full hover:bg-blue-700"
            onClick={() => setSidebarOpen(false)}
          >
            &#171;&#171;
          </button>
        </div>

        <div className="mb-4">
          <label className="block mb-1">Python Version</label>
          <select
            className="w-full p-2 rounded bg-gray-800 text-white"
            value={pythonVersion}
            onChange={e => setPythonVersion(e.target.value)}
          >
            {["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"].map(ver => (
              <option key={ver} value={ver}>{ver}</option>
            ))}
          </select>
        </div>

        <div className="mb-4">
          <label className="block mb-1">GitHub Repo Link</label>
          <input
            type="text"
            className="w-full p-2 rounded bg-gray-800 text-white"
            value={repoUrl}
            onChange={e => setRepoUrl(e.target.value)}
            onKeyDown = {handleFetch}
            placeholder="https://github.com/user/repo"
          />
          <span className="text-sm text-gray-400">Press Enter to fetch branches</span>
        </div>

        {branches.length > 0 && (
          <div className="mb-4">
            <label className="block mb-1">Branch</label>
            <select
              className="w-full p-2 rounded bg-gray-800 text-white"
              value={branch}
              onChange={e => setBranch(e.target.value)}
            >
              {branches.map(b => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>
        )}
      </div>
    </div>
  );
}
