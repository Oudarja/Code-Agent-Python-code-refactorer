'use client';

import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import React from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar"; // ✅ New import
import { RepoProvider } from "@/context/RepoContext"; // ✅ New import

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);
  const [pythonVersion, setPythonVersion] = React.useState("3.10");
  const [githubRepo, setGithubRepo] = React.useState("");
  const [branch, setBranch] = React.useState("main");

  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <RepoProvider>
          <Navbar
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
          />

          <Sidebar
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
            pythonVersion={pythonVersion}
            setPythonVersion={setPythonVersion}
            githubRepo={githubRepo}
            setGithubRepo={setGithubRepo}
            branch={branch}
            setBranch={setBranch}
          />
        {children}
        </RepoProvider>

      </body>
    </html>
  );
}
