'use client';

import React from "react";
import Link from "next/link";

export default function Navbar({ sidebarOpen, setSidebarOpen }) {
  return (
    <nav className="flex gap-15 justify-end mr-auto bg-gray-800 pt-4 pr-4 sticky top-0 z-50 shadow-lg p-4">
      {!sidebarOpen && (
        <button
          className="mr-auto px-3 py-1 bg-gray-900 text-white rounded-full hover:bg-blue-700 transition-colors "
          onClick={() => setSidebarOpen(true)}
          aria-label="Open Sidebar"
        >
          &#187;&#187;
        </button>
      )}
      <Link href="/" className="no-underline text-white hover:text-blue-600">Home</Link>
      <Link href="/overview" className="no-underline text-white hover:text-blue-600">Overview</Link>
      <Link href="/refactor" className="no-underline text-white hover:text-blue-600">Refactor</Link>
      <Link href="/analyzer" className="no-underline text-white hover:text-blue-600">Analyze</Link>
      <Link href="/dependency_management" className="no-underline text-white hover:text-blue-600">Dependency</Link>
      <Link href="/readme_generation" className="no-underline text-white hover:text-blue-600">Readme</Link>
      <Link href="/github_action" className="no-underline text-white hover:text-blue-600">GitHub</Link>
    </nav>
  );
}
