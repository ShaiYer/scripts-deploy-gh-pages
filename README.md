
# 🚀 Deploying Google AI Studio Projects to GitHub Pages

This guide provides step-by-step instructions for deploying React + Vite applications developed in Google AI Studio to GitHub Pages. Follow these instructions to install, run, deploy, and synchronize updates to your project.

## Examples

- [Example Google AI Studio Project](https://aistudio.google.com/app/apps/drive/1k0e6q34-_nZ_XzEbSErVRi9wplEL_OCZ?showPreview=true&resourceKey=) - A React application built with Google AI Studio
- [GitHub Repository Example](https://github.com/ShaiYer/react-robo-runner) - React Robo Run source code
- [Live GitHub Pages Demo](https://shaiyer.github.io/react-robo-runner/) - See the deployed application


---

## 🔧 1. Initial Setup

### Install dependencies

After downloading your project from Google AI Studio:

```bash
npm install
```

### Run the development server

To test your application locally:

```bash
npm run dev
```

Your application will be available at: [http://localhost:5173](http://localhost:5173)

---

## 🚀 2. Deployment to GitHub Pages

### Install the GitHub Pages deployment package

Add the required dependency for GitHub Pages deployment:

```bash
npm install --save-dev gh-pages
```

### Update `vite.config.ts`

Modify your `vite.config.ts` file to configure GitHub Pages deployment:

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

**Important:** Replace `<repo-name>` with your actual GitHub repository name (e.g., `'/react-robo-runner/'`). This sets the correct base path for your deployed application.

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

Before deploying to GitHub Pages, it's recommended to test your production build locally:

```bash
npm run build
npm run preview
```

Your preview will be available at:
```
http://localhost:4173/
```

⚠️ **Important Note**: The paths in your `dist/` folder are relative to the GitHub Pages URL (e.g., `/react-robo-runner/`). 
This means that directly opening the `index.html` file from the `dist` folder in your browser (via `file://` protocol) 
will **not work correctly**. Always use `npm run preview` to test the production build locally.

---

## 🔁 4. Synchronizing Updates from Google AI Studio

When you make changes to your project in Google AI Studio and download the updated code, follow these steps to safely update your GitHub repository without breaking the deployment setup.

### 🛠 Using the Provided Synchronization Script

This repository includes a Python script that automates the synchronization process with safety checks:

```bash
./run-sync-react-project.py --source=/path/to/downloaded/folder --target=/path/to/your/git/project --verbose
```

For a dry run (preview changes without applying):
```bash
./run-sync-react-project.py --source=/path/to/downloaded/folder --target=/path/to/your/git/project --dry-run --verbose
```

You can also create a configuration file (`config.ini`):
```ini
[DEFAULT]
source = /path/to/downloaded/folder
target = /path/to/your/git/project
```

And use it:
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

### 💡 Why We Exclude Certain Files

The synchronization process intentionally excludes the following files:

- `node_modules/`, `dist/`: Auto-generated directories that should not be copied
- `.git`, `.gitignore`: Prevent corruption of Git repository configuration
- `vite.config.ts`, `package.json`, `package-lock.json`: These contain build and deployment configurations — do not overwrite them unless you explicitly modified them in Google AI Studio

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

## 📋 Quick Reference

1. **Initial Setup**: `npm install` → `npm run dev`
2. **Configure for GitHub Pages**: Update `vite.config.ts` and `package.json`
3. **Deploy**: `npm run deploy`
4. **Update from Google AI Studio**: Run the sync script → commit changes → deploy again

## ✅ Conclusion

By following this guide, you can seamlessly develop applications in Google AI Studio and deploy them to GitHub Pages while maintaining a proper development workflow. The synchronization tools provided help you avoid common pitfalls when moving code between environments.
