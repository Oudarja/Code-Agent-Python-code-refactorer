'use client';

import React, { useState } from 'react';
import { commitPushRepository } from '@/lib/github_api'; // Import your API functions
import { useRepo } from '@/context/RepoContext'; // Import RepoContext for state management

const CommitAndPush = ({ owner, repo, setIsPrVisible }) => {
  const {branches, src_branch, setSrcBranch, commitMessage, setCommitMessage, pushMessage, setPushMessage } = useRepo();
  const [loading, setLoading] = useState(false);
  const [isBranchSelect, setIsBranchSelect] = useState(false); // Manage whether "Select Branch" or "Type Branch" is chosen

  const handleCommitAndPush = async () => {
    try {
      const selectedBranch = src_branch;
      if (!selectedBranch || !commitMessage) {
        alert('Source branch and commit message are required!');
        return;
      }

      setLoading(true);
      setPushMessage('');

      // Call the API to commit and push
      const result = await commitPushRepository(owner, repo, commitMessage, selectedBranch, 'main');
      console.log(result);
      setIsPrVisible(true);  // Show PR options after successful push
      setPushMessage('Push successful! You can now create a pull request.');
    } catch (error) {
      console.error('Error pushing commit:', error);
      setPushMessage('Failed to push the commit. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6 w-1/2 mx-auto">
      <h2 className="text-2xl mb-2 text-left">Commit and Push</h2>

      {/* Branch input toggle */}
      <div className="mb-4">
        <label htmlFor="branch" className="block mb-2 text-left">Source Branch:</label>
        <div className="flex gap-4">
          {/* Radio buttons for toggle */}
          <label className="p-2">
            <input 
              type="radio"
              name="branchToggle"
              checked={!isBranchSelect}
              onChange={() => {
                setIsBranchSelect(false); // User selects "Type Branch"
                setSrcBranch(''); // Clear the branch name if switching to input
              }}
            /> Type Branch
          </label>
          <label className="p-2">
            <input 
              type="radio"
              name="branchToggle"
              checked={isBranchSelect}
              onChange={() => {
                setIsBranchSelect(true); // User selects "Select Branch"
                setSrcBranch(''); // Clear the branch name if switching to select
              }}
            /> Select Branch
          </label>
        </div>

        {isBranchSelect ? (
          // Dropdown for selecting the destination branch (using the context branches)
          <select
            className="mt-2 p-2 bg-gray-800 text-gray-100 w-full"
            value={src_branch}
            onChange={(e) => setSrcBranch(e.target.value)} // Update src_branch based on selection
          >
            <option value="">Select a branch</option>
            {branches?.map((branch, index) => (
              <option key={index} value={branch}>
                {branch}
              </option>
            ))}
          </select>
        ) : (
          // Direct input for source branch name
          <input
            type="text"
            className="mt-2 p-2 bg-gray-800 w-full text-gray-100"
            placeholder="Enter source branch name"
            value={src_branch}
            onChange={(e) => setSrcBranch(e.target.value)} // Update the input value directly
          />
        )}
      </div>

      {/* Commit message */}
      <div className="mb-4">
        <label htmlFor="commitMessage" className="block mb-2 text-left">Commit Message:</label>
        <input
          type="text"
          className="p-2 bg-gray-800 w-full text-gray-100"
          placeholder="Enter commit message"
          value={commitMessage}
          onChange={(e) => setCommitMessage(e.target.value)}
        />
      </div>

      {/* Commit & Push Button */}
      <div className="text-center">
        <button
          className="bg-blue-600 p-2 rounded text-white w-full"
          onClick={handleCommitAndPush}
          disabled={loading}
        >
          {loading ? 'Pushing...' : 'Commit and Push'}
        </button>
        {/* Push Message */}
        {pushMessage && (
          <div className="mt-2 text-center text-gray-300">{pushMessage}</div>
        )}
      </div>
    </div>
  );
};

export default CommitAndPush;
