'use client'; 

import React, { useState } from 'react';
import { useRepo } from '@/context/RepoContext';  // Assuming you have a RepoContext for state management
import CommitAndPush from '@/components/CommitAndPush'; // Import your CommitAndPush component
import CreatePR from '@/components/CreatePR'; // Import your CreatePR component

export default function Home() {
  const { owner, repo, branches } = useRepo();
  const [isPrVisible, setIsPrVisible] = useState(false);
  const [src_branch, setSrcBranch] = useState('');

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100 mt-0 px-10">
      {/* Header Section */}
      <h1 className="text-4xl font-bold mb-4 text-blue-400 text-center">GitHub Action Tab</h1>

      {/* Commit & Push Section */}
      <CommitAndPush owner={owner} repo={repo} setIsPrVisible={setIsPrVisible} setSrcBranch={setSrcBranch} />

      {/* PR Section (Visible after successful push) */}
      {isPrVisible && <CreatePR owner={owner} repo={repo} src_branch={src_branch} />}
    </div>
  );
}
