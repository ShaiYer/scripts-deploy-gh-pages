# Embedding a React App Inside an Angular Component

This document explains how to embed an AI-built React application inside an Angular component, including bundling, styling, and server updates.

---

## 1. 🧩 React App Preparation

### a. Build with Vite as IIFE
In your React app (`vite.react-angular.config.ts`), configure the build as an Immediately Invoked Function Expression (IIFE) with a global export:

#### To Run specific config of vite
```bash
npx vite build --config vite.react-angular.config.ts
```

```ts
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '');
  return {
    plugins: [react()],
    build: {
      lib: {
        entry: './index.tsx',
        name: 'RoboRunner',
        formats: ['iife'],
        fileName: () => `robo-runner.iif.js`,
      },
      outDir: 'dist',
      rollupOptions: {
        output: {
          globals: {
            react: 'React',
            'react-dom': 'ReactDOM',
          },
        },
      },
    },
    define: {
      'process.env': {
        NODE_ENV: JSON.stringify(mode || 'development'),
        API_KEY: JSON.stringify(env.GEMINI_API_KEY || ''),
        GEMINI_API_KEY: JSON.stringify(env.GEMINI_API_KEY || ''),
      }
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
  };
});
```

### b. Define Global Renderer
Expose your React renderer globally in `index.tsx`:

```ts
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

declare global {
    interface Window {
        renderReactApp?: (containerId: string, props?: any) => { unmount?: () => void };
    }
}

window.renderReactApp = function (containerId: string, props = {}) {
    const container = document.getElementById(containerId);
    if (!container) {
        throw new Error(\`Container element '\${containerId}' not found\`);
    }

    const root = ReactDOM.createRoot(container);
    root.render(<App {...props} />);
    return {
        unmount: () => root.unmount()
    };
};
```

Ensure `index.tsx` still supports development:

```ts
if (import.meta.env.DEV) {
  const rootEl = document.getElementById('root');
  if (rootEl) {
    ReactDOM.createRoot(rootEl).render(<App />);
  }
}
```

### c. Embed Styles in React
Add Tailwind CSS and custom variables in `index.html` of your React app:

```html
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root {
    --color-background: #111827;
    --robot-body-color: #f3f4f6;
    ...
  }
  .h-screen {
    height: auto !important;
  }
  .w-screen {
    width: 100%;
  }
  .min-h-screen {
    min-height: 100vh;
  }
</style>
```

---

## 2. 🧱 Angular Component Setup

### a. Component Definition
In Angular create `robo-runner-wrapper.component.ts`:

```ts
@Component({
  selector: 'app-robo-runner-wrapper',
  templateUrl: './robo-runner-wrapper.component.html',
  styleUrls: ['./robo-runner-wrapper.component.scss']
})
export class RoboRunnerWrapperComponent implements AfterViewInit, OnDestroy {
  @ViewChild('reactContainer') containerRef!: ElementRef;
  private root: any;

  async ngAfterViewInit() {
    await this.loadScript('/assets/react/robo-runner.iif.js');
    this.root = window.renderReactApp?.('react-root');
  }

  private loadScript(src: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (document.querySelector(\`script[src="\${src}"]\`)) return resolve();

      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve();
      script.onerror = () => reject(\`Failed to load \${src}\`);
      document.body.appendChild(script);
    });
  }

  ngOnDestroy() {
    this.root?.unmount?.();
  }
}
```

### b. Template HTML
```html
<div #reactContainer id="react-root" style="width: 100%; height: auto;"></div>
```

---

## 3. 🌐 Laravel Server Update

### a. Update Route
```php
Route::get('/{app}/assets/{any}', [ClientAppsController::class, 'catchAllAppsAssets'])->where('any', '.*');
```

### b. Update Controller Logic
```php
if (file_exists($filePath)) {
    $mimeType = (str_ends_with($filePath, '.iif.js')) ? 'application/javascript' : mime_content_type($filePath);
    return response(file_get_contents($filePath))->header('Content-Type', $mimeType);
}
```

---

## 4. 📁 Directory Structure Suggestion

```
public/
└── assets/
    └── react/
        └── robo-runner.iif.js

angular-app/
└── src/
    └── app/
        └── robo-runner-wrapper/
            ├── robo-runner-wrapper.component.ts
            └── robo-runner-wrapper.component.html
```

---

## 5. 🧪 Test

Visit the Angular route where the component is used and ensure:
- Script loads
- Game UI is visible and responsive
- Styling (Tailwind + Custom) is correctly applied

---

## ✅ Done

You now have an AI-built React app (like a game or component) embedded and styled inside your Angular application!
