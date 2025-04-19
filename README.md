# 🚀 TooBig: Find Your Chunky Code Files 🚀

Ever feel like your codebase is getting a bit... *chonky*? `toobig.py` is here to help you vibe check your project and spot those hefty **code files** that might need a little refactoring love. ✨

It intelligently scans your current directory (while skipping common non-code directories like `node_modules`, `.git`, `build`, etc., and ignoring binary files, images, archives, etc.), counts up the relevant text files, lines, and characters, and points out the biggest bois. Keep your code lean and mean! 💪

## 🤔 Why?

Big source code files can be a drag. They're harder to read, harder to maintain, and just generally mess with the coding flow. `toobig.py` helps you identify potential candidates for splitting into smaller, more manageable pieces. Keep it modular, keep it cool. 😎

## ✨ How to Use

It's super simple! Just curl the script directly from the repo and run it with Python in the root of your project directory:

```bash
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3
```

## 🧠 What it Skips

To keep things fast and relevant, `toobig.py` skips:

*   **Common Directories:** `.git`, `node_modules`, `venv`, `__pycache__`, `build`, `dist`, `target`, `.vscode`, `.idea`, and more.
*   **Non-Code Files:** Images (`.png`, `.jpg`...), archives (`.zip`, `.tar`...), binaries (`.exe`, `.dll`...), compiled code (`.pyc`, `.class`...), documents (`.pdf`, `.docx`...), media (`.mp4`, `.mp3`...), fonts, logs, and minified files (`.min.js`, `.min.css`).

This focuses the analysis on the files you're most likely to edit and refactor.

## 📊 Example Output

Running the script will give you something like this:

```plaintext
Analyzing repository in /path/to/your/project...
Scanning: /path/to/your/project/some/sub/directory        
Analysis Results:
Total number of files analyzed: 157
Total number of lines of text: 25890
Total number of characters: 987654

Top 5 Largest Files:
------------------------------------------------------------
#1 src/mega_component.js
Size: 150.34 KB
Lines: 3050
Characters: 153987
------------------------------------------------------------
#2 tests/integration/heavy_test_suite.py
Size: 95.12 KB
Lines: 1800
Characters: 97412
------------------------------------------------------------
#3 assets/styles/huge_stylesheet.css
Size: 88.76 KB
Lines: 2100
Characters: 90888
------------------------------------------------------------
#4 data/big_seed_file.json
Size: 75.45 KB
Lines: 500
Characters: 77250
------------------------------------------------------------
#5 docs/massive_spec.md
Size: 60.91 KB
Lines: 1500
Characters: 62380
------------------------------------------------------------
```

Now go forth and refactor! ✂️ 
