'use client';

import React, { useState } from 'react';
import { createGitPR } from '@/lib/github_api'; // Import your API functions
import { useRepo } from '@/context/RepoContext'; // Import RepoContext for state management

const CreatePR = ({ owner, repo }) => {
    const { src_branch, dest_branch, prTitle, setPrTitle, prBody, setPrBody, prMessage, setPrMessage } = useRepo();
    const [loadingPr, setLoadingPr] = useState(false);

    const handleCreatePR = async () => {
    try {
      if (!prTitle || !prBody) {
        alert('PR title and body are required!');
        return;
      }

      setLoadingPr(true);
      setPrMessage('');

      const baseBranch = 'main';  // Can dynamically use the repo base branch here

      const prResult = await createGitPR(owner, repo, src_branch, baseBranch, prTitle, prBody);
      console.log('PR created successfully:', prResult);

      // Optionally, you can display the PR URL in the UI
      setPrMessage(`PR created successfully: ${prResult}`);
    } catch (error) {
      console.error('Error creating PR:', error);
      setPrMessage('Failed to create PR. Please try again.');
    } finally {
      setLoadingPr(false);
    }
  };

  return (
    <div className="mt-8 w-1/2 mx-auto">
      <h2 className="text-2xl mb-2 text-left">Create Pull Request</h2>

      {/* Source branch (pre-filled) */}
      <div className="mb-4">
        <label className="block mb-2 text-left">Source Branch:</label>
        <input
          type="text"
          className="p-2 bg-gray-800 w-full text-gray-100"
          value={src_branch}
          readOnly
        />
      </div>

      {/* Destination branch (select from context) */}
      <div className="mb-4">
        <label className="block mb-2 text-left">Destination Branch:</label>
        <select
          className="p-2 bg-gray-800 w-full text-gray-100"
          value={dest_branch}
          onChange={(e) => setDestBranch(e.target.value)}
        >
          <option value="">Select destination branch</option>
          {/* Add your branch options here */}
        </select>
      </div>

      {/* PR Title and Body */}
      <div className="mb-4">
        <label className="block mb-2 text-left">PR Title:</label>
        <input
          type="text"
          className="p-2 bg-gray-800 w-full text-gray-100"
          placeholder="Enter PR title"
          value={prTitle}
          onChange={(e) => setPrTitle(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <label className="block mb-2 text-left">PR Body:</label>
        <textarea
          className="p-2 bg-gray-800 w-full text-gray-100"
          placeholder="Enter PR body"
          value={prBody}
          onChange={(e) => setPrBody(e.target.value)}
        />
      </div>

      {/* Create PR Button */}
      <div className="text-center">
        <button
          className="bg-green-600 p-2 rounded text-white w-full"
          onClick={handleCreatePR}
          disabled={loadingPr}
        >
          {loadingPr ? 'Creating PR...' : 'Create Pull Request'}
        </button>
      </div>

      {/* PR Message */}
      {prMessage && (
        <div className="mt-2 text-center text-gray-300">{prMessage}</div>
      )}
    </div>
  );
};

export default CreatePR;
