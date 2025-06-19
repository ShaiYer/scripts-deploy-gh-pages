#!/usr/bin/env python3
"""
run-rsync-project.py

A Python script to synchronize files between a source and target directory using rsync,
with built-in safety checks, config file support, and index.html validation.

No external dependencies are used — compatible with bare Python 3 installations.

Usage examples:
    ./run-rsync-project.py --source=./exported --target=./project -n -v
    ./run-rsync-project.py --config=config.ini
"""

import argparse
import os
import subprocess
import configparser
import sys

def confirm_index_exists(folder, label):
    """Check that index.html exists in the specified folder"""
    index_path = os.path.join(folder, "index.html")
    if not os.path.isfile(index_path):
        print(f"Warning: index.html not found in {label} ({folder})")
        try:
            response = input("Continue anyway? [y/N]: ").strip().lower()
        except KeyboardInterrupt:
            print()
            sys.exit(1)
        if response != 'y':
            print("Aborted by user.")
            sys.exit(1)

def load_config(path):
    """Load source/target values from a config file if provided"""
    config = configparser.ConfigParser()
    config.read(path)
    result = {}
    if 'DEFAULT' in config:
        default = config['DEFAULT']
        if 'source' in default:
            result['source'] = default['source']
        if 'target' in default:
            result['target'] = default['target']
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Sync project files using rsync with safety checks.",
        epilog="Example: ./run-rsync-project.py --source=./src --target=./dst -n -v"
    )
    parser.add_argument('--source', '-s', help='Source directory (default: current directory)', default=None)
    parser.add_argument('--target', '-t', help='Target directory (default: current directory)', default=None)
    parser.add_argument('--dry-run', '-n', action='store_true', help='Perform a dry run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--config', '-c', help='Path to config file (INI format with [DEFAULT] section)')

    args = parser.parse_args()

    # Set defaults to current working directory if not provided
    source = args.source or os.getcwd()
    target = args.target or os.getcwd()

    # Override with config file if provided
    if args.config:
        if not os.path.isfile(args.config):
            print(f"Error: Config file not found: {args.config}")
            sys.exit(1)
        config_data = load_config(args.config)
        source = config_data.get('source', source)
        target = config_data.get('target', target)

    # Ensure at least one of source or target is valid
    if not source and not target:
        print("Error: Either source or target must be provided.")
        sys.exit(1)

    # Confirm both source and target contain index.html
    confirm_index_exists(source, "source")
    confirm_index_exists(target, "target")

    # Construct the rsync command with exclusions
    rsync_cmd = [
        "rsync", "-av",
        "--exclude=node_modules",
        "--exclude=dist",
        "--exclude=.git",
        "--exclude=.gitignore",
        "--exclude=vite.config.ts",
        "--exclude=package.json",
        "--exclude=package-lock.json",
    ]

    # Add dry-run flag if requested
    if args.dry_run:
        rsync_cmd.append("--dry-run")

    # Add source and target directories
    rsync_cmd.append(f"{source}/")
    rsync_cmd.append(f"{target}/")

    # Verbose output
    if args.verbose:
        print(f"Source: {source}")
        print(f"Target: {target}")
        print(f"Running command: {' '.join(rsync_cmd)}")

    # Execute the rsync command
    try:
        subprocess.run(rsync_cmd, check=True)
        print("Rsync operation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Rsync operation failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
