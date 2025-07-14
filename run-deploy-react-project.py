#!/usr/bin/env python3
"""
run-deploy.py

A Python script to help with various deployment tasks for React projects,
including configuration for GitHub Pages and bundle generation.

No external dependencies are used — compatible with bare Python 3 installations.

Usage examples:
    ./run-deploy.py --action=add-config-gh-pages --app-base-path=/user/repo/
    ./run-deploy.py --action=build-gh-pages
    ./run-deploy.py --config=config.ini
"""

import argparse
import os
import subprocess
import configparser
import sys
import shutil
import json

def load_config(path):
    """Load configuration values from a config file if provided"""
    config = configparser.ConfigParser()
    config.read(path)
    result = {}
    if 'DEFAULT' in config:
        default = config['DEFAULT']
        for key in default:
            result[key] = default[key]
    return result

def get_user_action_choice():
    """Prompt user to select an action"""
    actions = [
        "add-config-gh-pages", 
        "add-config-bundle", 
        "build-gh-pages", 
        "deploy-gh-pages", 
        "generate-bundle",
        "update-index-tsx",
        "generate-config",
        "deploy-next-gh-pages"
    ]

    print("Please select an action:")
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")

    while True:
        try:
            choice = input("Enter the number of your choice: ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(actions):
                return actions[choice_idx]
            else:
                print(f"Please enter a number between 1 and {len(actions)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print()
            sys.exit(1)

def create_gh_pages_config(app_base_path, verbose=False, dry_run=False):
    """Create vite.gh-pages.config.ts file"""
    config_file = "vite.gh-pages.config.ts"

    # Check if file already exists
    if os.path.exists(config_file):
        print(f"Error: {config_file} already exists. Aborting.")
        sys.exit(1)

    if verbose:
        print(f"Preparing to create {config_file} with app base path: {app_base_path}")

    # Create the file with the specified content
    content = f"""import path from 'path';
import {{ defineConfig, loadEnv }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({{ mode }}) => {{
    const env = loadEnv(mode, '.', '');

    return {{
        base: '{app_base_path}', // required for GitHub Pages
        plugins: [react()],
        define: {{}},
        resolve: {{
            alias: {{
                '@': path.resolve(__dirname, '.'),
            }},
        }},
    }};
}});
"""

    if dry_run:
        print(f"[DRY RUN] Would create {config_file} with app base path: {app_base_path}")
    else:
        with open(config_file, 'w') as f:
            f.write(content)
        print(f"Created {config_file} with app base path: {app_base_path}")

    return True

def create_bundle_config(app_name, verbose=False, dry_run=False):
    """Create vite.react-angular.config.ts file"""
    config_file = "vite.react-angular.config.ts"

    # Check if file already exists
    if os.path.exists(config_file):
        print(f"Error: {config_file} already exists. Aborting.")
        sys.exit(1)

    # Create dashed version and capitalized version of app name
    app_name_dashed = app_name.replace(' ', '-').lower()
    app_name_caps = ''.join(word.capitalize() for word in app_name.split('-'))

    if verbose:
        print(f"Preparing to create {config_file} with app name: {app_name}")
        print(f"App name dashed: {app_name_dashed}")
        print(f"App name capitalized: {app_name_caps}")

    # Create the file with the specified content
    content = f"""import path from 'path';
import {{ defineConfig, loadEnv }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({{ mode }}) => {{
    const env = loadEnv(mode, '.', '');

    return {{
        plugins: [react()],
        build: {{
            outDir: 'dist',
            emptyOutDir: true,
            lib: {{
                entry: './index.tsx',
                name: '{app_name_caps}',
                formats: ['iife'],
                fileName: () => `{app_name_dashed}.iif.js`,
            }},
            rollupOptions: {{
                // Keep everything bundled (no externals!)
                external: [],
                output: {{
                    globals: {{
                        react: 'React',
                        'react-dom': 'ReactDOM',
                    }},
                }},
            }},
        }},
        define: {{
            'process.env': {{
                NODE_ENV: JSON.stringify(mode || 'development'),
                API_KEY: JSON.stringify(env.GEMINI_API_KEY || ''),
                GEMINI_API_KEY: JSON.stringify(env.GEMINI_API_KEY || ''),
            }},
        }},
        resolve: {{
            alias: {{
                '@': path.resolve(__dirname, '.'),
            }},
        }},
    }};
}});
"""

    if dry_run:
        print(f"[DRY RUN] Would create {config_file} with app name: {app_name}")
        print(f"[DRY RUN] App name dashed: {app_name_dashed}")
        print(f"[DRY RUN] App name capitalized: {app_name_caps}")
    else:
        with open(config_file, 'w') as f:
            f.write(content)
        print(f"Created {config_file} with app name: {app_name}")
        print(f"App name dashed: {app_name_dashed}")
        print(f"App name capitalized: {app_name_caps}")

    return True

def build_gh_pages(verbose=False, dry_run=False):
    """Build the project for GitHub Pages"""
    config_file = "vite.gh-pages.config.ts"

    # Check if config file exists
    if not os.path.exists(config_file):
        print(f"Error: {config_file} not found. Please run --action=add-config-gh-pages first.")
        sys.exit(1)

    if verbose:
        print(f"Config file {config_file} exists, proceeding with build")

    # Prepare the build command
    build_cmd = ["vite", "build", "--config", config_file]

    # Execute the build command
    try:
        if dry_run:
            print(f"[DRY RUN] Would execute: {' '.join(build_cmd)}")
            print("[DRY RUN] Build would be completed")
        else:
            print("Building project for GitHub Pages...")
            if verbose:
                print(f"Executing: {' '.join(build_cmd)}")
            subprocess.run(build_cmd, check=True)
            print("Build completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with exit code {e.returncode}.")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'vite' command not found. Make sure Vite is installed.")
        sys.exit(1)

def deploy_gh_pages(verbose=False, dry_run=False):
    """Deploy the project to GitHub Pages"""
    # Prepare the deploy command
    deploy_cmd = ["npm", "run", "build-gh-pages"]

    try:
        if dry_run:
            print(f"[DRY RUN] Would execute: {' '.join(deploy_cmd)}")
            print("[DRY RUN] Deployment would be completed")
        else:
            print("Deploying to GitHub Pages...")
            if verbose:
                print(f"Executing: {' '.join(deploy_cmd)}")
            subprocess.run(deploy_cmd, check=True)
            print("Deployment completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Deployment failed with exit code {e.returncode}.")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'npm' command not found. Make sure npm is installed.")
        sys.exit(1)


# New Area for next scripts
def deploy_next_gh_pages(app_base_path, verbose=False, dry_run=False):
    """Deploy Next.js project to GitHub Pages"""

    local_config = "next.config.ts"
    backup_config = "next.config.org.ts"
    template_config_name = "config-next.config.ts"
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Backup existing local config if exists
    if os.path.exists(local_config):
        if verbose:
            print(f"Backing up {local_config} to {backup_config}")
        if not dry_run:
            shutil.move(local_config, backup_config)

    # Step 2: Check if local config already exists (after backup, it doesn't)
    local_config_exists = os.path.exists(local_config)

    if not local_config_exists:
        if not app_base_path:
            print("[ERROR] Missing app_base_path (repo name). Exiting.")
            sys.exit(1)

        template_path = os.path.join(script_dir, template_config_name)
        if not os.path.exists(template_path):
            print(f"[ERROR] Template config file not found: {template_path}")
            sys.exit(1)

        # Read and modify template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace("const repo = 'repo-name';", f"const repo = '{app_base_path}';")

        if verbose:
            print(f"Writing modified config to {local_config}")
        if dry_run:
            print("[DRY RUN] Would write the following content:")
            print(content)
        else:
            with open(local_config, 'w', encoding='utf-8') as f:
                f.write(content)

    else:
        if verbose:
            print(f"Reusing existing config file: {local_config}")

    # Ensure next.config.ts exists now
    if not os.path.exists(local_config):
        print(f"[ERROR] Local config file {local_config} was not created.")
        sys.exit(1)

    print(f"[SUCCESS] Local Next.js config is ready: {local_config}")

    # Step 3: Update package.json scripts
    package_file = "package.json"
    if not os.path.exists(package_file):
        print("[ERROR] package.json not found in current directory")
        sys.exit(1)

    with open(package_file, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        scripts = data.get("scripts", {})

        modified = False
        if "export" not in scripts:
            scripts["export"] = "next export"
            modified = True
        if "predeploy" not in scripts:
            scripts["predeploy"] = "npm run build && touch out/.nojekyll"
            modified = True
        if "deploy" not in scripts:
            scripts["deploy"] = "gh-pages -d out"
            modified = True

        if modified:
            if verbose:
                print("Updating package.json scripts")
            if not dry_run:
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            else:
                print("[DRY RUN] Would update package.json scripts:")
                print(json.dumps(scripts, indent=2))

    # Step 4: Run predeploy and deploy
    if dry_run:
        print("[DRY RUN] Would run: npm run predeploy")
        print("[DRY RUN] Would run: npm run deploy")
    else:
        try:
            print("Running: npm run predeploy")
            subprocess.run(["npm", "run", "predeploy"], check=True)
            print("Running: npm run deploy")
            subprocess.run(["npm", "run", "deploy"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Deployment failed with exit code {e.returncode}")
            sys.exit(e.returncode)

    print("[SUCCESS] Deployment to GitHub Pages completed.")
    return True




def get_dir_deploy_script():
    return os.path.dirname(os.path.abspath(__file__))

def get_dir_current_folder():
    return os.path.abspath(os.getcwd())


def get_file_path(file_name, is_dir_deploy_script=True):
    # Create the file with the specified content

    if is_dir_deploy_script:
        script_dir = get_dir_deploy_script()
    else:
        script_dir = get_dir_current_folder()

    file_path = os.path.join(script_dir, file_name)

    print(file_path)

    if os.path.exists(file_path):
        return file_path

    return False


# end Area for next deploy

def generate_bundle(verbose=False, dry_run=False):
    """Generate a bundle using the react-angular config"""
    config_file = "vite.react-angular.config.ts"

    # Check if config file exists
    if not os.path.exists(config_file):
        print(f"Error: {config_file} not found. Please run --action=add-config-bundle first.")
        sys.exit(1)

    if verbose:
        print(f"Config file {config_file} exists, proceeding with bundle generation")

    # Prepare the build command
    build_cmd = ["vite", "build", "--config", config_file]

    # Execute the build command
    try:
        if dry_run:
            print(f"[DRY RUN] Would execute: {' '.join(build_cmd)}")
            print("[DRY RUN] Bundle generation would be completed")
        else:
            print("Generating bundle...")
            if verbose:
                print(f"Executing: {' '.join(build_cmd)}")
            subprocess.run(build_cmd, check=True)
            print("Bundle generation completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Bundle generation failed with exit code {e.returncode}.")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'vite' command not found. Make sure Vite is installed.")
        sys.exit(1)

def generate_config(verbose=False, dry_run=False):
    """Generate config-deploy.conf file for deployment configuration"""
    index_file = "index.tsx"
    config_file = "config-deploy.conf"

    # Check if index.tsx exists
    if not os.path.exists(index_file):
        print(f"Error: {index_file} not found. Not a React folder with {os.getcwd()}")
        sys.exit(1)

    # Check if config-deploy.conf already exists
    if os.path.exists(config_file):
        print(f"Error: {config_file} already exists.")
        sys.exit(1)

    if verbose:
        print(f"Preparing to create {config_file}")

    # Create the file with the specified content
    script_dir = os.path.dirname(os.path.abspath(__file__))
    example_config = os.path.join(script_dir, 'config-deploy-example.conf')
    
    with open(example_config, 'r') as f:
        content = f.read()

    if dry_run:
        print(f"[DRY RUN] Would create {config_file}")
    else:
        try:
            with open(config_file, 'w') as f:
                f.write(content)
            print(f"Successfully created {config_file}")
            return True
        except Exception as e:
            print(f"Error creating file: {str(e)}")
            sys.exit(1)

    return True

def update_index_tsx(verbose=False, dry_run=False):
    """Update index.tsx file with the template for React deployment"""
    index_file = "index.tsx"
    backup_file = "index.org.tsx"
    template_file = "index.deploy.template.tsx"

    # Check if index.tsx exists
    if not os.path.exists(index_file):
        print(f"Error: {index_file} not found. This action requires an existing index.tsx file.")
        sys.exit(1)

    # Check if template file exists
    if not os.path.exists(template_file):
        print(f"Error: {template_file} not found. This action requires the template file.")
        sys.exit(1)

    if verbose:
        print(f"Found {index_file}, proceeding with update")

    # Create backup
    if dry_run:
        print(f"[DRY RUN] Would create backup of {index_file} as {backup_file}")
    else:
        try:
            with open(index_file, 'r') as src:
                content = src.read()
            with open(backup_file, 'w') as dst:
                dst.write(content)
            if verbose:
                print(f"Created backup of {index_file} as {backup_file}")
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            sys.exit(1)

    # Display confirmation message
    message = "This will update the index.tsx file. It will work for dev + load tailwind (if not exist) and ready for react wrap with angular. Would you like to continue? (y/n) [n]: "

    if dry_run:
        print(f"[DRY RUN] Would prompt: {message}")
        print("[DRY RUN] Update would be completed if confirmed")
        return True

    # Get user confirmation
    confirmation = input(message).strip().lower()
    if confirmation != 'y':
        print("Update cancelled.")
        return False

    # Replace content with template
    try:
        with open(template_file, 'r') as src:
            template_content = src.read()
        with open(index_file, 'w') as dst:
            dst.write(template_content)
        print(f"Successfully updated {index_file} with content from {template_file}")
        return True
    except Exception as e:
        print(f"Error updating file: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Deploy React projects to GitHub Pages and generate bundles.",
        epilog="Example: ./run-deploy.py --action=add-config-gh-pages --app-base-path=/user/repo/"
    )
    parser.add_argument('--action', choices=[
        'add-config-gh-pages', 
        'add-config-bundle', 
        'build-gh-pages', 
        'deploy-gh-pages', 
        'generate-bundle',
        'update-index-tsx',
        'generate-config',
        'deploy-next-gh-pages'
    ], help='Action to perform')
    parser.add_argument('--app-base-path', help='Base path for GitHub Pages (e.g., /user/repo/)')
    parser.add_argument('--app-name', help='Application name for bundle generation')
    parser.add_argument('--config', '-c', help='Path to config file (INI format with [DEFAULT] section)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Perform a dry run')
    parser.add_argument('--no-config', action='store_true', help='Skip loading the default config file')

    args = parser.parse_args()

    # Initialize configuration
    config = {}

    if args.verbose:
        print('start main')

    # Check for default config file if --no-config is not specified and --config is not provided
    script_dir = get_dir_current_folder()
    default_config = os.path.join(script_dir, 'config-deploy.conf')
    if args.verbose:
        print(default_config)
    if not args.no_config and not args.config and os.path.isfile(default_config):
        if args.verbose:
            print(f"Loading default config file: {default_config}")
        config = load_config(default_config)

    # Override with explicit config file if provided
    if args.config:
        if not os.path.isfile(args.config):
            print(f"Error: Config file not found: {args.config}")
            sys.exit(1)
        config = load_config(args.config)

    # Get action from args or prompt user
    action = args.action
    if not action:
        action = get_user_action_choice()

    # Get app_base_path from args or config
    app_base_path = args.app_base_path or config.get('app_base_path')

    # Get app_name from args or config
    app_name = args.app_name or config.get('app_name')

    # Execute the selected action
    if action == 'add-config-gh-pages':
        if not app_base_path:
            app_base_path = input("Enter the app base path (e.g., /user/repo/): ").strip()
        create_gh_pages_config(app_base_path, verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'add-config-bundle':
        if not app_name:
            # Suggest current folder name as default
            current_folder = os.path.basename(os.getcwd())
            app_name = input(f"Enter the app name (default: {current_folder}): ").strip()
            if not app_name:
                app_name = current_folder
        create_bundle_config(app_name, verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'build-gh-pages':
        build_gh_pages(verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'deploy-gh-pages':
        deploy_gh_pages(verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'generate-bundle':
        generate_bundle(verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'update-index-tsx':
        update_index_tsx(verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'generate-config':
        generate_config(verbose=args.verbose, dry_run=args.dry_run)

    elif action == 'deploy-next-gh-pages':
        print('deploy-next-gh-pages')
        if not app_base_path:
                    print("[ERROR] Missing app_base_path (repo name). Exiting.")
                    sys.exit(1)
        deploy_next_gh_pages(app_base_path, verbose=args.verbose, dry_run=args.dry_run)
if __name__ == "__main__":
    main()
