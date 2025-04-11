#!/usr/bin/env python3
"""
GitHub Text File Uploader

This script uploads text files from a local directory to a GitHub repository.
It works well with the output from extract_pdf_text.py.

Requirements:
    pip install PyGithub
"""

import os
import sys
import argparse
from github import Github
import base64
from pathlib import Path

def upload_files_to_github(token, repo_name, local_dir, github_dir=None, file_ext='.txt'):
    """Upload all text files from local_dir to GitHub repository."""
    try:
        # Connect to GitHub
        g = Github(token)
        
        # Get the repository
        repo = g.get_repo(repo_name)
        print(f"Connected to repository: {repo.full_name}")
        
        # Prepare the file list
        files_to_upload = []
        for root, _, files in os.walk(local_dir):
            for file in files:
                if file.endswith(file_ext):
                    local_path = os.path.join(root, file)
                    # Calculate relative path
                    rel_path = os.path.relpath(local_path, local_dir)
                    
                    # Determine GitHub path
                    if github_dir:
                        github_path = os.path.join(github_dir, rel_path).replace('\\', '/')
                    else:
                        github_path = rel_path.replace('\\', '/')
                    
                    files_to_upload.append((local_path, github_path))
        
        if not files_to_upload:
            print(f"No {file_ext} files found in {local_dir}")
            return False
        
        # Upload each file
        for local_path, github_path in files_to_upload:
            try:
                print(f"Uploading {local_path} to {github_path}...")
                
                # Read file content
                with open(local_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Check if file already exists
                try:
                    existing_file = repo.get_contents(github_path)
                    # Update existing file
                    repo.update_file(
                        path=github_path,
                        message=f"Update {os.path.basename(github_path)}",
                        content=content,
                        sha=existing_file.sha
                    )
                    print(f"Updated existing file: {github_path}")
                except Exception:
                    # Create new file
                    repo.create_file(
                        path=github_path,
                        message=f"Add {os.path.basename(github_path)}",
                        content=content
                    )
                    print(f"Created new file: {github_path}")
            
            except Exception as e:
                print(f"Error uploading {local_path}: {e}")
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Upload text files to GitHub repository.')
    parser.add_argument('local_dir', help='Local directory containing text files')
    parser.add_argument('repo_name', help='GitHub repository name (format: username/repo)')
    parser.add_argument('-t', '--token', help='GitHub Personal Access Token (PAT)')
    parser.add_argument('-g', '--github_dir', help='Directory in the GitHub repository (default: repository root)')
    parser.add_argument('-e', '--extension', default='.txt', help='File extension to upload (default: .txt)')
    
    args = parser.parse_args()
    
    # Get GitHub token
    token = args.token
    if not token:
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            token = input("Enter your GitHub Personal Access Token: ")
    
    if not os.path.isdir(args.local_dir):
        print(f"Error: {args.local_dir} is not a valid directory")
        return 1
    
    success = upload_files_to_github(
        token=token,
        repo_name=args.repo_name,
        local_dir=args.local_dir,
        github_dir=args.github_dir,
        file_ext=args.extension
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
