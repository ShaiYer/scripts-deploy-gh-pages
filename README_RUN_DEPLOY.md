# 🚀 Run Deploy Script Documentation

## Overview

The `run-deploy.py` script is a versatile tool designed to streamline the deployment process for React projects, particularly for GitHub Pages deployment and bundle generation. This script automates several common tasks in the deployment workflow, making it easier to configure and deploy your React applications.

## Features

- Create GitHub Pages configuration files
- Create bundle configuration files for React applications
- Build projects for GitHub Pages deployment
- Deploy projects to GitHub Pages
- Generate bundles for integration with other applications
- Support for configuration files to store common settings
- Interactive mode when no action is specified

## Prerequisites

- Python 3.x
- Node.js and npm (for deployment and build operations)
- Vite (for build operations)

## Installation

No installation is required. Simply download the script and make it executable:

```bash
chmod +x run-deploy-react-project.py
```

## Usage

### Basic Usage

```bash
./run-deploy-react-project.py --action=<action> [options]
```

If no action is specified, the script will enter interactive mode and prompt you to select an action.

### Available Actions

#### 1. add-config-gh-pages

Creates a Vite configuration file (`vite.gh-pages.config.ts`) for GitHub Pages deployment.

```bash
./run-deploy-react-project.py --action=add-config-gh-pages --app-base-path=/user/repo/
```

If `--app-base-path` is not provided, the script will prompt you to enter it.

#### 2. add-config-bundle

Creates a Vite configuration file (`vite.react-angular.config.ts`) for bundle generation.

```bash
./run-deploy-react-project.py --action=add-config-bundle --app-name=my-app
```

If `--app-name` is not provided, the script will suggest the current folder name as default and prompt you to confirm or change it.

#### 3. build-gh-pages

Builds the project for GitHub Pages deployment using the `vite.gh-pages.config.ts` configuration.

```bash
./run-deploy-react-project.py --action=build-gh-pages
```

This action requires that the `vite.gh-pages.config.ts` file exists.

#### 4. deploy-gh-pages

Deploys the project to GitHub Pages by running the `npm run build-gh-pages` command.

```bash
./run-deploy-react-project.py --action=deploy-gh-pages
```

This action assumes that you have configured the `build-gh-pages` script in your `package.json` file.

#### 5. generate-bundle

Generates a bundle using the `vite.react-angular.config.ts` configuration.

```bash
./run-deploy-react-project.py --action=generate-bundle
```

This action requires that the `vite.react-angular.config.ts` file exists.

### Configuration Options

#### Command-Line Options

- `--action`: The action to perform (one of the actions listed above)
- `--app-base-path`: The base path for GitHub Pages deployment (e.g., `/user/repo/`)
- `--app-name`: The application name for bundle generation
- `--config`, `-c`: Path to a configuration file (INI format with [DEFAULT] section)
- `--verbose`, `-v`: Enable verbose output (prints detailed information during execution)
- `--dry-run`, `-n`: Perform a dry run (shows what would happen without making actual changes)
- `--no-config`: Skip loading the default configuration file

#### Configuration File

You can store common settings in a configuration file (INI format) to avoid typing them repeatedly. The script will automatically look for a file named `config-deploy.conf` in the same directory as the script, unless the `--no-config` flag is specified.

Example configuration file:

```ini
[DEFAULT]
app_base_path = /my-project/
app_name = my-awesome-app
```

You can also specify a custom configuration file using the `--config` option:

```bash
./run-deploy-react-project.py --action=add-config-gh-pages --config=my-config.ini
```

## Examples

### Create GitHub Pages Configuration

```bash
./run-deploy-react-project.py --action=add-config-gh-pages --app-base-path=/my-project/
```

This will create a `vite.gh-pages.config.ts` file with the specified base path.

### Create Bundle Configuration

```bash
./run-deploy-react-project.py --action=add-config-bundle --app-name=my-app
```

This will create a `vite.react-angular.config.ts` file with the specified application name.

### Build and Deploy to GitHub Pages

```bash
./run-deploy-react-project.py --action=build-gh-pages
./run-deploy-react-project.py --action=deploy-gh-pages
```

These commands will build the project for GitHub Pages and then deploy it.

### Generate a Bundle

```bash
./run-deploy-react-project.py --action=generate-bundle
```

This will generate a bundle using the `vite.react-angular.config.ts` configuration.

### Using Verbose and Dry Run Options

#### Verbose Output

Use the `--verbose` or `-v` flag to get detailed information during execution:

```bash
./run-deploy-react-project.py --action=build-gh-pages --verbose
```

This will show additional information such as:
- Configuration file loading
- File existence checks
- Command execution details

#### Dry Run Mode

Use the `--dry-run` or `-n` flag to see what would happen without making actual changes:

```bash
./run-deploy-react-project.py --action=deploy-gh-pages --dry-run
```

This will show what commands would be executed without actually running them.

#### Combining Options

You can combine both options to get detailed information in dry run mode:

```bash
./run-deploy-react-project.py --action=add-config-bundle --app-name=my-app --verbose --dry-run
```

This is useful for testing and understanding the script's behavior before making actual changes.

## Troubleshooting

### Common Issues

1. **File Already Exists**: If the configuration file you're trying to create already exists, the script will exit with an error. You'll need to manually delete or rename the existing file before running the script again.

2. **Command Not Found**: If you encounter a "command not found" error, make sure you have the required dependencies installed (Node.js, npm, Vite).

3. **Build or Deployment Failures**: If the build or deployment process fails, check the error message for details. Common issues include missing dependencies or configuration errors.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.
