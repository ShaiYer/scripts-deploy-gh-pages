# 🚀 Deploying a Next.js Static Site to GitHub Pages

This guide explains how to configure, build, and deploy a statically exported Next.js site to GitHub Pages.

---

## 📦 Prerequisites

- A GitHub repository (e.g., `https://github.com/yourusername/your-repo`)
- Node.js and npm installed
- Your Next.js project set up and working

---

## 🛠️ Step 1: Install `gh-pages`

This package will publish your static files to the `gh-pages` branch.

```bash
npm install --save-dev gh-pages
```

---
## Switch to branch deploy and make changes to the config
```bash
$ git checkout deploy
```

---


## ⚙️ Step 2: Configure `next.config.js`

Create or modify your `next.config.js` to include:

```typescript
// next.config.js
import type { NextConfig } from 'next';

const repo = 'repo-name';

const nextConfig: NextConfig = {
   output: 'export',
   basePath: `/${repo}`,
   assetPrefix: `/${repo}/`,
   trailingSlash: true,

   typescript: {
      ignoreBuildErrors: true,
   },
   eslint: {
      ignoreDuringBuilds: true,
   },
   images: {
      unoptimized: true,
      remotePatterns: [
         {
            protocol: 'https',
            hostname: 'placehold.co',
            port: '',
            pathname: '/**',
         },
      ],
   },
};

module.exports = nextConfig;

```

Replace `your-repo` with the name of your GitHub repository.

---

## 📁 Step 3: Add Scripts to `package.json` or run manually

Update your `package.json` with the following scripts:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "export": "next export",
    "predeploy": "npm run build && npm run export && touch out/.nojekyll",
    "deploy": "gh-pages -d out"
  }
}
```

> 📝 `touch out/.nojekyll` ensures that GitHub Pages will not ignore the `_next` folder (critical for serving assets correctly).

---

## 🧱 Step 4: Build and Deploy

### If script are not added to the 'package.json'
```bash
npm run build && touch out/.nojekyll
npx gh-pages -d out
```



```bash
npm run predeploy
npm run deploy
```

This will:
1. Build your Next.js app
2. Export it to the `out/` folder
3. Add a `.nojekyll` file to prevent GitHub from hiding the `_next` directory
4. Push the contents of `out/` to the `gh-pages` branch

---

## 🌍 Step 5: Configure GitHub Pages

1. Go to your GitHub repo settings
2. Scroll to **Pages**
3. Choose:
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
4. Save

Your site will be live at:
```
https://yourusername.github.io/your-repo/
```

---

## 🧩 Troubleshooting

- ❌ **CSS/JS 404 errors**: Make sure `.nojekyll` is present in the root of the deployed `out/` directory.
- ❌ **Wrong asset paths**: Verify `basePath` and `assetPrefix` are correctly set in `next.config.js`.
- ❌ **404 for pages**: GitHub Pages doesn't support client-side routing. Use only statically generated routes.
- ❌ **For local dev and view** - copy index.html to index-local.html with correct paths - no base href

---

## ✅ Example Repo Structure

```
your-repo/
├── .next/
├── out/
│   ├── _next/
│   ├── index.html
│   └── .nojekyll  ✅
├── pages/
│   └── index.js
├── next.config.js
└── package.json
```

---

## 🔗 References

- [Next.js - Static HTML Export](https://nextjs.org/docs/pages/building-your-application/deploying/static-exports)
- [gh-pages - npm](https://www.npmjs.com/package/gh-pages)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

---

Happy shipping! 🚀
