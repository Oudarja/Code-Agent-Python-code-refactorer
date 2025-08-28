'use client';

export default function Home() {
  return (
    <div className="bg-gray-900 text-white min-h-screen">
      {/* Header Section */}
      <header className="text-center py-10">
        <h1 className="text-4xl font-bold mb-4">Code Agent</h1>
        <p className="text-xl text-gray-400">A powerful tool for automated code analysis, refactoring, and GitHub integration.</p>
      </header>

      {/* About Section */}
      <section className="px-6 md:px-16 py-10">
        <h2 className="text-3xl font-semibold mb-6 text-center">About Code Agent</h2>
        <p className="text-lg text-gray-300">
          Code Agent is an intelligent tool designed to automate code analysis, refactoring, and management tasks for Python projects. 
          By leveraging the power of Large Language Models (LLMs), it can detect issues, refactor legacy code, generate test cases, 
          update dependencies, and seamlessly integrate with GitHub to push changes and create pull requests.
        </p>
      </section>

      {/* Features Section */}
      <section className="bg-gray-800 px-6 md:px-16 py-10">
        <h2 className="text-3xl font-semibold mb-6 text-center text-blue-400">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">Code Analyzer</h3>
            <p className="text-gray-300">
              Detects outdated syntax, anti-patterns, hardcoded values, and maintainability issues in your Python code.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">Code Refactorer</h3>
            <p className="text-gray-300">
              Refactors legacy or modern Python code (`3.x`) into more idiomatic and optimized code using LLMs.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">Documentation Generator</h3>
            <p className="text-gray-300">
              Generates Pythonic docstrings and documentation for functions, classes, and modules to improve code readability.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">Code Diff Viewer</h3>
            <p className="text-gray-300">
              View side-by-side comparisons of original vs. refactored code to easily track changes.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">Requirements Updater</h3>
            <p className="text-gray-300">
              Updates your `requirements.txt` to the latest compatible versions of packages.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">README Generator</h3>
            <p className="text-gray-300">
              Automatically generates a detailed README for your project, summarizing files, functions, and the overall structure.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">Runtime Validator</h3>
            <p className="text-gray-300">
              Creates a virtual environment and installs updated dependencies to validate the refactored code in real-time.
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow">
            <h3 className="text-xl font-semibold mb-4">GitHub Integration</h3>
            <p className="text-gray-300">
              - Analyze GitHub repositories and branches. <br />
              - Refactor and push code to a new branch. <br />
              - Create pull requests with title and description for seamless collaboration.
            </p>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="bg-gray-800 py-6 mt-12">
        <div className="text-center text-gray-400">
          <p>&copy; 2025 Code Agent. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
