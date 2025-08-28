'use client';

import React, { createContext, useContext, useState } from 'react';

const RepoContext = createContext();

export function RepoProvider({ children }) {
  const [pythonVersion, setPythonVersion] = useState("3.12");
  const [repoUrl, setRepoUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [branch, setBranch] = useState("");
  const [branches, setBranches] = useState([]);
  const [files, setFiles] = useState([]);
  const [installedPackages, setInstalledPackages] = useState();
  const [refactoredRepoContents, setRefactoredRepoContents] = useState({});
  const [logs, setLogs] = useState([]);
  const [src_branch, setSrcBranch] = useState('');
  const [commitMessage, setCommitMessage] = useState('');
  const [pushMessage, setPushMessage] = useState('');
  const [dest_branch, setDestBranch] = useState('');
  const [prTitle, setPrTitle] = useState('');
  const [prBody, setPrBody] = useState('');
  const [prMessage, setPrMessage] = useState('');

  return (
    <RepoContext.Provider
      value={{
        pythonVersion, setPythonVersion,
        repoUrl, setRepoUrl,
        owner, setOwner,
        repo, setRepo,
        branch, setBranch,
        branches, setBranches,
        files, setFiles,
        installedPackages, setInstalledPackages,
        refactoredRepoContents, setRefactoredRepoContents,
        logs, setLogs,
        src_branch, setSrcBranch,
        commitMessage, setCommitMessage,
        pushMessage, setPushMessage,
        dest_branch, setDestBranch,
        prTitle, setPrTitle,
        prBody, setPrBody,
        prMessage, setPrMessage
      }}
    >
      {children}
    </RepoContext.Provider>
  );
}

export function useRepo() {
  return useContext(RepoContext);
}
