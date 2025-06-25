
# 🚀 Guide to implement AI studio project to GitHub Pages - project React + Vite Deployment 

This document provides step-by-step instructions to install, run, deploy, and sync updates to a React + Vite app hosted on GitHub Pages.

## Implementation examples

[Google AI project built with React](https://aistudio.google.com/app/apps/drive/1k0e6q34-_nZ_XzEbSErVRi9wplEL_OCZ?showPreview=true&resourceKey=)


[GitHub project - React Robo Run](https://github.com/ShaiYer/react-robo-runner)

[GitHub pages example - React Robo Run](https://shaiyer.github.io/react-robo-runner/)


---

## 🔧 1. Initial Setup

### Install dependencies

```bash
npm install
```

### Run the development server

```bash
npm run dev
```

App will be available at: [http://localhost:5173](http://localhost:5173)

---

## 🚀 2. Deployment to GitHub Pages

### Install the GitHub Pages deployment package

```bash
npm install --save-dev gh-pages
```

### Update `vite.config.ts`

Edit `vite.config.ts` to include:

```ts
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '');

  return {
    base: '/<repo-name>/', // e.g., '/react-robo-runner/'
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

Replace `<repo-name>` with your actual GitHub repo name.

### Add deploy scripts to `package.json`

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "predeploy": "npm run build",
  "deploy": "gh-pages -d dist"
}
```

### Add `.gitignore`

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

### Deploy

```bash
npm run deploy
```

App will be available at:
```
https://<your-username>.github.io/<repo-name>/
```

---

## 🔍 3. Test Production Build Locally

To preview the build before deploying:

```bash
npm run build
npm run preview
```

Preview will be available at:
```
http://localhost:4173/
```

⚠️ Paths in the `dist/` folder will be relative to the GitHub Pages URL (e.g., `/react-robo-runner/`). So testing by opening `index.html` in the browser (via `file://`) will **not work** correctly — use `npm run preview`.

---

## 🔁 4. Sync with Google AI Studio Updates

When downloading new code from **Google AI Studio**, follow this process to avoid breaking the repo setup.

### 🛠 Recommended `rsync` usage

From the downloaded folder:

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

### 💡 Why exclude these files?

- `node_modules/`, `dist/`: Auto-generated, shouldn't be copied
- `.git`, `.gitignore`: Prevents corrupting git config
- `vite.config.ts`, `package.json`: These contain build & deploy configuration — do not overwrite them unless you explicitly updated them in AI Studio

### ✅ After syncing:

From your Git project directory:

```bash
git add .
git commit -m "Sync updated code from AI Studio"
git push
```

Then deploy again if needed:

```bash
npm run deploy
```

---

## ✅ Done!

Your project is now synced, tested, and deployed to GitHub Pages.
