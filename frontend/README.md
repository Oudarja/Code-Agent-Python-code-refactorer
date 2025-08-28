# Code Agent – Frontend

**CodeAgent** is an AI-powered developer assistant that analyzes, refactors, tests, and documents Python code from GitHub repositories. It helps improve code quality and developer productivity using LLMs (Large Language Models) like Groq's LLaMA models.

---
## Project Structure

```python
frontend/
├── .next/                      # Build output (auto-generated)
├── app/                        # App router directory
│ ├── analyzer/                 # Route: /analyzer
│ │ └── page.js
│ ├── dependency_management/    # Route: /dependency_management
│ │ └── page.js
│ ├── github_action/            # Route: /github_action
│ │ └── page.js
│ ├── overview/                 # Route: /overview
│ │ └── page.js
│ ├── readme_generation/        # Route: /readme_generation
│ │ └── page.js
│ ├── refactor/                 # Route: /refactor
│ │ └── page.js
│ ├── globals.css               # Global styles
│ ├── layout.js                 # Root layout (applies to all routes)
│ └── page.js                   # Root page (e.g., index route)
├── lib/                        # Reusable logic, API helpers, hooks
├── node_modules/               # Installed dependencies
├── public/                     # Static files (images, icons)
├── .gitignore                  # Git exclusions
├── next-env.d.ts               # TypeScript env declarations
├── next.config.ts              # Next.js config (TypeScript)
├── package.json                # Project metadata and scripts
├── package-lock.json           # Dependency lock file
├── postcss.config.mjs          # PostCSS config (for Tailwind, etc.)
├── tsconfig.json               # TypeScript configuration
└── README.md                   # Project documentation
```


##  Project Features

- Built with **Next.js**
- Custom UI for input and result display
- Integrates with backend `api` of LLMs

---

## Project Setup

Follow these steps to run the frontend on a new machine.

### 1. Prerequisites

- Node.js **v22.17.1**(Recommended: LTS)
- npm (comes with Node)
- Git

**Check versions :**
```bash
node -v
npm -v
```


### 2. Clone the Repository
```bash
git clone git@gitlab.com:cloudlyio/code-agent.git
cd code-agent/frontend
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Run the Development Server
```bash
npm run dev
```
