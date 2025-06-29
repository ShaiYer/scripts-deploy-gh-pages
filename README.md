
# 🚀 Guide: Continuous Deployment of Google AI Studio Projects to GitHub Pages

This guide provides step-by-step instructions for deploying React + Vite applications developed in Google AI Studio to GitHub Pages and synchronizing project changes. Follow these instructions to install dependencies, run your application locally, deploy to GitHub Pages, and maintain updates between environments.


Google AI Studio projects don't support direct Git integration, making version control and deployment challenging. This guide solves that problem with a streamlined workflow.


This workflow solves the challenge of developing in Google AI Studio while leveraging GitHub Pages for deployment. By following this guide:

1. You can build applications in Google AI Studio's rich development environment
2. Safely synchronize code changes without breaking your deployment configuration
3. Maintain version control via GitHub
4. Deploy and share your applications publicly through GitHub Pages

The synchronization tools and workflow provided here eliminate common issues when working across these different environments, allowing you to focus on developing your application rather than managing deployment complexities.



  
  
## Example References

- [Example Google AI Studio Project](https://aistudio.google.com/app/apps/drive/1k0e6q34-_nZ_XzEbSErVRi9wplEL_OCZ?showPreview=true&resourceKey=) - A React application built with Google AI Studio
- [GitHub Repository Example](https://github.com/ShaiYer/react-robo-runner) - React Robo Run source code
- [Live GitHub Pages Demo](https://shaiyer.github.io/react-robo-runner/) - See the deployed application

---

## Workflow Overview

1. Develop your application in Google AI Studio
2. Download your project files
3. Follow this guide to configure and deploy to GitHub Pages
4. Use the provided synchronization tools when updating your project



## 🔧 1. Initial Setup

### Install dependencies the GitHub Pages deployment package

Navigate to your project directory and install the required dependencies:

```bash
cd ./your-project
npm install
```

Add the required dependency for GitHub Pages deployment:

```bash
npm install --save-dev gh-pages
npm install --save-dev @vitejs/plugin-react
```


### Run the development server

Test your application locally to ensure it works correctly:

```bash
npm run dev
```

Your application will be available at: [http://localhost:5173](http://localhost:5173)

---

## 🚀 2. Deployment to GitHub Pages


### Update `vite.config.ts`

Modify your `vite.config.ts` file to configure GitHub Pages deployment. The key change is setting the correct base path:

```ts
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '');

  return {
    base: '/<repo-name>/', // IMPORTANT: Replace with your GitHub repository name
    plugins: [react()],
    define: {
      'process.env.API_KEY': JSON.stringify(env.GEMINI_API_KEY),
      'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY)
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
  };
});
```

**Critical Step:** Replace `<repo-name>` with your actual GitHub repository name (e.g., `'/react-robo-runner/'`). This configures the correct base path for your GitHub Pages deployment and ensures all assets load properly.

### Add deployment scripts to `package.json`

Add the following scripts to your `package.json` file:

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "predeploy": "npm run build",
  "deploy": "gh-pages -d dist"
}
```

The `predeploy` script automatically runs before `deploy`, ensuring your project is built before deployment.

### Create or update `.gitignore`

Create a `.gitignore` file with the following content to exclude unnecessary files from your repository:

```gitignore
node_modules/
dist/
.vite/
.env*
.DS_Store
.vscode/
.idea/
*.log
```

### Deploy to GitHub Pages

Run the deployment command:

```bash
npm run deploy
```

After successful deployment, your application will be available at:
```
https://<your-username>.github.io/<repo-name>/
```

Where `<your-username>` is your GitHub username and `<repo-name>` is your repository name.

---

## 🔍 3. Testing Your Production Build Locally

Before deploying to GitHub Pages, test your production build locally to catch any potential issues:

```bash
npm run build
npm run preview
```

Your preview will be available at:
```
http://localhost:4173/
```

⚠️ **Important Warning**: The paths in your `dist/` folder are relative to the GitHub Pages URL (e.g., `/react-robo-runner/`). 
Because of this path configuration:

1. Directly opening the `index.html` file from the `dist` folder in your browser (via `file://` protocol) will **not work correctly**
2. Assets like images, CSS, and JavaScript files will fail to load when opened directly
3. Always use `npm run preview` to properly simulate the GitHub Pages environment locally

---

## 🔁 4. Synchronizing Updates from Google AI Studio

When you make changes to your project in Google AI Studio, you'll need to synchronize those changes with your GitHub repository without breaking the deployment setup. This section explains how to do that safely.

### 🛠 Using the Provided Synchronization Script

This repository includes a Python script (`run-sync-react-project.py`) that automates the synchronization process with built-in safety checks:

```bash
./run-sync-react-project.py --source=/path/to/downloaded/folder --target=/path/to/your/git/project --verbose
```

#### Script Options:

* **Dry Run Mode** - Preview changes without applying them:
  ```bash
  ./run-sync-react-project.py --source=/path/to/downloaded/folder --target=/path/to/your/git/project --dry-run --verbose
  ```

* **Configuration File** - Save your settings in a `config.ini` file:
  ```ini
  [DEFAULT]
  source = /path/to/downloaded/folder
  target = /path/to/your/git/project
  ```

  Then use it with:
  ```bash
  ./run-sync-react-project.py --config=config.ini --verbose
  ```

### 🛠 Manual Synchronization with `rsync`

If you prefer to use `rsync` directly, run the following command from your downloaded folder:

```bash
rsync -av --exclude='node_modules' \
          --exclude='dist' \
          --exclude='.git' \
          --exclude='.gitignore' \
          --exclude='vite.config.ts' \
          --exclude='package.json' \
          --exclude='package-lock.json' \
          ./ /path/to/your/git/project/
```

### 💡 Understanding File Exclusions

The synchronization process intentionally excludes specific files and directories for the following reasons:

| Excluded Item | Reason |
|---------------|--------|
| `node_modules/`, `dist/` | Auto-generated directories that should not be copied; they are environment-specific |
| `.git`, `.gitignore` | Prevents corruption of your Git repository configuration |
| `vite.config.ts` | Contains your GitHub Pages path configuration that should be preserved |
| `package.json`, `package-lock.json` | Contains your deployment scripts and dependency specifications |

**Warning:** Only overwrite these excluded files if you intentionally modified them in Google AI Studio and understand the implications.

### ✅ After Synchronization

Once you've synchronized your files, commit the changes to your repository:

```bash
cd /path/to/your/git/project
git add .
git commit -m "Sync updated code from Google AI Studio"
git push
```

Then deploy the updated version to GitHub Pages:

```bash
npm run deploy
```

---

## 📋 Quick Reference Guide

| Step | Action | Commands |
|------|--------|----------|
| 1. Initial Setup | Install and test locally | `npm install` → `npm run dev` |
| 2. Configure for GitHub Pages | Update config files | Edit `vite.config.ts` and `package.json` |
| 3. Deploy | Build and deploy to GitHub Pages | `npm run deploy` |
| 4. Sync Updates | Get latest changes from AI Studio | `./run-sync-react-project.py --source=/path/to/downloaded --target=/path/to/repo --verbose` |
| 5. Redeploy | Deploy after syncing changes | `git add .` → `git commit -m "Sync updates"` → `git push` → `npm run deploy` |



