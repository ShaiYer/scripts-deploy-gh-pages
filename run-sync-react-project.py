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
import random

def get_random_number():
    """Return a random integer between 1 and 100"""
    return random.randint(1, 100)

def confirm_index_exists(folder, label):
    """Check that index.html exists in the specified folder"""
    index_path = os.path.join(os.path.abspath(folder), "index.html") 
    if not os.path.isfile(index_path):
        print(f"Warning: index.html not found in {label} ({index_path})")
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
        if 'ignore_index_tsx' in default:
            result['ignore_index_tsx'] = default.getboolean('ignore_index_tsx', fallback=False)
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
    parser.add_argument('--no-config', action='store_true', help='Skip loading the default config file')

    args = parser.parse_args()

    # Set defaults to current working directory if not provided
    source = args.source or os.getcwd()
    target = args.target or os.getcwd()

    # Strip any surrounding quotes from source and target paths
    if source and ((source.startswith('"') and source.endswith('"')) or (source.startswith("'") and source.endswith("'"))):
        source = source[1:-1]
    if target and ((target.startswith('"') and target.endswith('"')) or (target.startswith("'") and target.endswith("'"))):
        target = target[1:-1]

    # Check for default config file if --no-config is not specified and --config is not provided
    # Look for the config file in the current working directory
    default_config = os.path.join(os.getcwd(), 'config-deploy.conf')
    if not args.no_config and not args.config:
        if args.verbose:
            print(f"Trying to reach config file at: {default_config}")
        if os.path.isfile(default_config):
            if args.verbose:
                print(f"Config file found. Loading default config file: {default_config}")
            config_data = load_config(default_config)
            # Only use source/target from config if not provided as arguments
            if args.source is None:
                source = config_data.get('source', source)
                # Strip any surrounding quotes from source path loaded from config
                if source and ((source.startswith('"') and source.endswith('"')) or (source.startswith("'") and source.endswith("'"))):
                    source = source[1:-1]
                if args.verbose and 'source' in config_data:
                    print(f"Using source from config file: {source}")
            if args.target is None:
                target = config_data.get('target', target)
                # Strip any surrounding quotes from target path loaded from config
                if target and ((target.startswith('"') and target.endswith('"')) or (target.startswith("'") and target.endswith("'"))):
                    target = target[1:-1]
                if args.verbose and 'target' in config_data:
                    print(f"Using target from config file: {target}")
        elif args.verbose:
            print(f"Config file not found at: {default_config}")

    # Override with explicit config file if provided
    if args.config:
        if args.verbose:
            print(f"Trying to reach config file at: {args.config}")
        if not os.path.isfile(args.config):
            print(f"Error: Config file not found: {args.config}")
            sys.exit(1)
        if args.verbose:
            print(f"Config file found. Loading config file: {args.config}")
        config_data = load_config(args.config)
        # Only use source/target from config if not provided as arguments
        if args.source is None:
            source = config_data.get('source', source)
            # Strip any surrounding quotes from source path loaded from config
            if source and ((source.startswith('"') and source.endswith('"')) or (source.startswith("'") and source.endswith("'"))):
                source = source[1:-1]
            if args.verbose and 'source' in config_data:
                print(f"Using source from config file: {source}")
        if args.target is None:
            target = config_data.get('target', target)
            # Strip any surrounding quotes from target path loaded from config
            if target and ((target.startswith('"') and target.endswith('"')) or (target.startswith("'") and target.endswith("'"))):
                target = target[1:-1]
            if args.verbose and 'target' in config_data:
                print(f"Using target from config file: {target}")

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

    # Add index.tsx to exclusions if configured
    ignore_index_tsx = config_data.get('ignore_index_tsx', False) if 'config_data' in locals() else False
    if ignore_index_tsx:
        rsync_cmd.append("--exclude=index.tsx")
        if args.verbose:
            print("Excluding index.tsx from sync as configured")

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
