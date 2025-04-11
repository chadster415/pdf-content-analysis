#!/usr/bin/env python3
"""
PDF Text Extractor

This script extracts text from PDF files in a specified directory and 
saves the text content to text files in the same or a different directory.

Requirements:
    pip install PyPDF2
"""

import os
import sys
import argparse
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Some pages might be images or have no text
                text += page_text + "\n\n"
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

def process_directory(input_dir, output_dir=None, recursive=False):
    """Process all PDF files in a directory."""
    if output_dir is None:
        output_dir = input_dir
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get all PDF files in the directory
    pdf_files = []
    if recursive:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
    else:
        pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) 
                     if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(input_dir, f))]
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    # Process each PDF file
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Create output file path
            rel_path = os.path.relpath(pdf_path, input_dir) if recursive else os.path.basename(pdf_path)
            txt_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + '.txt')
            
            # Create directories if needed
            os.makedirs(os.path.dirname(txt_path), exist_ok=True)
            
            # Write text to file
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            print(f"Text extracted and saved to {txt_path}")
        else:
            print(f"Failed to extract text from {pdf_path}")

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files.')
    parser.add_argument('input_dir', help='Directory containing PDF files')
    parser.add_argument('-o', '--output_dir', help='Directory to save text files (default: same as input)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Process subdirectories recursively')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory")
        return 1
    
    process_directory(input_dir, args.output_dir, args.recursive)
    return 0

if __name__ == "__main__":
    sys.exit(main())
