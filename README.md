# PDF Content Analysis

This repository contains tools to extract text from PDF files and upload them to GitHub for analysis.

## Setup

1. Clone this repository:
```
git clone https://github.com/chadster415/pdf-content-analysis.git
cd pdf-content-analysis
```

2. Install required dependencies:
```
pip install PyPDF2 PyGithub
```

## Scripts

### 1. Extract Text from PDFs

The `extract_pdf_text.py` script converts PDF files to text files:

```
python extract_pdf_text.py /path/to/your/pdfs/
```

Options:
- `-o, --output_dir`: Specify output directory (default: same as input)
- `-r, --recursive`: Process subdirectories recursively

### 2. Upload Text Files to GitHub

The `upload_to_github.py` script uploads text files to this GitHub repository:

```
python upload_to_github.py /path/to/extracted/text/ chadster415/pdf-content-analysis -t YOUR_GITHUB_TOKEN
```

Options:
- `-t, --token`: GitHub Personal Access Token (can be set as GITHUB_TOKEN environment variable)
- `-g, --github_dir`: Directory within the repository to upload to (default: root)
- `-e, --extension`: File extension to upload (default: .txt)

## Complete Workflow Example

```bash
# 1. Extract text from all PDFs in a directory
python extract_pdf_text.py ~/Documents/my_pdfs/ -o ~/Documents/extracted_text/

# 2. Upload all extracted text files to GitHub
python upload_to_github.py ~/Documents/extracted_text/ chadster415/pdf-content-analysis
```

## Analyzing the Content

Once your text files are uploaded to the repository, you can:

1. Use GitHub search to find content across files
2. Ask questions about the content through Claude
3. Perform further analysis with other tools

## Repository Structure

- `*.txt`: Extracted text files from PDFs
- `extract_pdf_text.py`: Script to convert PDFs to text
- `upload_to_github.py`: Script to upload text files to GitHub
