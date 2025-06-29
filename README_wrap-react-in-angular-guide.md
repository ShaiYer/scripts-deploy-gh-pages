# Embedding a React App Inside an Angular Component


```
Updated version in wrap-react-with-angular.md
```



This document explains how to embed an AI-built React application inside an Angular component, including bundling, styling, and server updates.

---

## 1. 🧩 React App Preparation

### a. Build with Vite as IIFE
In your React app (`vite.config.ts`), configure the build as an Immediately Invoked Function Expression (IIFE) with a global export:


#### To Run specific config of vite
```bash
npx vite build --config vite.react-angular.config.ts
```


```ts
export default defineConfig({
  build: {
    lib: {
      entry: './index.tsx',
      name: 'RoboRunner',
      formats: ['iife'],
      fileName: () => `robo-runner.iif.js`,
    },
    outDir: 'dist',
  }
});
```

### b. Define Global Renderer
Expose your React renderer globally in `index.tsx`:

```ts
declare global {
  interface Window {
    renderRoboRunner?: (containerId: string, props?: any) => any;
  }
}

window.renderRoboRunner = (containerId: string, props?: any) => {
  const container = document.getElementById(containerId);
  return createRoot(container!).render(<App {...props} />);
};
```

### c. Embed Styles
Add all required Tailwind and custom CSS into the `index.html` file of the React project:

```html
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root {
    --color-background: #111827;
    --robot-body-color: #f3f4f6;
    ...
  }
  body {
    background-color: var(--color-background);
  }
</style>
```

---

## 2. 🧱 Angular Component Setup

### a. Component Definition
Create a wrapper Angular component (`robo-runner-wrapper.component.ts`):

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
    window.renderRoboRunner?.('react-root');
  }

  private loadScript(src: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`script[src="${src}"]`)) return resolve();

      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve();
      script.onerror = () => reject(`Failed to load ${src}`);
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
<div #reactContainer id="react-root" style="width: 100%; height: 100%;"></div>
```

---

## 3. 🌐 Laravel Server Update

Ensure the Laravel server serves the IIFE JS bundle with correct MIME type:

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

You now have an AI-built React game embedded and styled correctly in your Angular app!
