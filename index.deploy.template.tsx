
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Declare a global interface for a generic render object on the window.
// This allows different React apps to be attached without polluting the global scope.
declare global {
    interface Window {
        renderReact?: {
            [key: string]: (containerId: string) => { unmount: () => void };
        };
    }
}

/**
 * Renders the React application. This is wrapped in a function so it can be called
 * as a callback after ensuring all dependencies (like Tailwind) are loaded.
 */
const renderApplication = () => {
    // Ensure the global renderReact object exists before attaching the app-specific renderer.
    if (!window.renderReact) {
        window.renderReact = {};
    }

    /**
     * Renders the Ostrich Runner React application into a specific container.
     * This function is attached to a global object to serve as the entry point
     * for embedding the app in other frameworks (e.g., Angular).
     * @param containerId The ID of the DOM element where the app should be mounted.
     * @returns An object with an `unmount` function to clean up and remove the app.
     */
    window.renderReact.renderOstrichRunner = (containerId: string) => {
        const container = document.getElementById(containerId);
        if (!container) {
            throw new Error(`Could not find container element with id '${containerId}'`);
        }
        const root = ReactDOM.createRoot(container);
        root.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>
        );

        return {
            unmount: () => root.unmount(),
        };
    };

    // Auto-render the app if a 'root' element is found in the HTML.
    // This ensures the application can still run as a standalone page
    // when index.html is loaded directly.
    const rootElement = document.getElementById('root');
    if (rootElement) {
        const root = ReactDOM.createRoot(rootElement);
        root.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>
        );
    }
};

/**
 * Checks if Tailwind CSS is loaded by testing a specific utility class.
 * This test is more robust than checking for a generic class like 'hidden'
 * because it verifies a specific style (a shade of red) that is unique to Tailwind.
 * If not loaded, it dynamically injects the Tailwind CDN script into the document head
 * and waits for it to load before calling the provided callback.
 */
const ensureTailwindIsLoaded = (callback: () => void) => {
    // Create a temporary, invisible element to test styles on.
    const testEl = document.createElement('div');
    // Use a specific Tailwind class that is unlikely to be defined elsewhere.
    testEl.className = 'text-red-500';
    // Hide the element from view and prevent layout shifts, but allow styles to be computed.
    testEl.style.position = 'absolute';
    testEl.style.visibility = 'hidden';
    document.body.appendChild(testEl);

    // Check the computed style for the specific color Tailwind applies.
    const styles = window.getComputedStyle(testEl);
    // Tailwind's `text-red-500` corresponds to rgb(239, 68, 68).
    const isTailwindLoaded = styles.color === 'rgb(239, 68, 68)';

    // Clean up the test element.
    document.body.removeChild(testEl);

    // If Tailwind is not loaded, inject the script and wait for it to load.
    if (!isTailwindLoaded) {
        console.warn('Tailwind CSS not detected. Loading from CDN...');
        const script = document.createElement('script');
        script.src = 'https://cdn.tailwindcss.com';
        script.onload = () => {
            console.log('Tailwind CSS loaded from CDN.');
            callback();
        };
        document.head.appendChild(script);
    } else {
        // If already loaded, execute the callback immediately.
        callback();
    }
};

// Run the check and render the React application only after Tailwind is confirmed to be loaded.
ensureTailwindIsLoaded(renderApplication);
