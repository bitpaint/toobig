# 🚀 TooBig: Find Your Chunky Code Files 🚀

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

## 🚀 Quick Start

No installation needed! Just pipe it directly from GitHub using `curl` in the root of your project directory:

```bash
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3
```

This will scan the current directory (`.`) and show the top 5 largest files.
(See **Usage & Options** below for more customization.)

---

Ever feel like your codebase is getting a bit... *chonky*? `toobig.py` is a lightweight, zero-dependency Python script to help you vibe check your project and spot those hefty **code files** that might need a little refactoring love. ✨

It intelligently scans your directory, skipping common non-code directories (`node_modules`, `.git`, `build`, etc.) and file types (binaries, images, archives), counts up the relevant text files, lines, and characters, and points out the biggest offenders. Keep your code lean and mean! 💪

## 🤔 Why?

Large source code files can be a drag. They're harder to read, harder to maintain, slower to process by tools, and can generally mess with the coding flow. `toobig.py` helps you quickly identify potential candidates for splitting into smaller, more manageable modules. Keep it modular, keep it cool. 😎

## ✨ Features

*   **Fast Scan:** Intelligently skips irrelevant directories and file types.
*   **Zero Dependencies:** Runs anywhere with Python 3.6+ installed.
*   **Respects `.gitignore`:** Automatically ignores files and directories listed in your `.gitignore` (can be disabled with `--no-gitignore`).
*   **Configurable:** Use command-line arguments to customize behavior.
*   **Clear Output:** Shows total counts and highlights the largest files by size (KB/MB) in a clean, boxed format.

## ⚙️ Usage & Options

You can pass arguments directly after `python3 --` when using the `curl` method, or save the script and run it conventionally.

```bash
# Pipe arguments via curl
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3 -- [options] [directory]

# Or save and run
# wget https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py
# python toobig.py [options] [directory]
```

**Available Options:**

*   `directory`: The target directory to analyze (defaults to the current directory).
*   `--top N`: Show the top `N` largest files (default: `5`).
*   `--exclude-dirs PAT1,PAT2,...`: Comma-separated list of *additional* directory name patterns to exclude (e.g., `my_build_artifacts,temp*`). Uses simple `fnmatch` patterns.
*   `--exclude-exts .ext1,.ext2,...`: Comma-separated list of *additional* file extensions to exclude (must include the leading dot, e.g., `.log,.tmp`).
*   `--no-gitignore`: Do not read or respect `.gitignore` files.
*   `-v`, `--verbose`: Show potentially binary/unreadable files that are skipped during the scan.
*   `-h`, `--help`: Show the help message and exit.

**Examples:**

```bash
# Scan './src' directory, show top 10 files
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3 -- --top 10 ./src

# Scan current dir, exclude logs and temp files, show skipped files
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3 -- --exclude-exts .log,.tmp -v

# Scan current dir, also exclude any 'cache' directories
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3 -- --exclude-dirs cache

# Scan current dir, but ignore the .gitignore file
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3 -- --no-gitignore
```

## 🧠 What it Skips By Default

To keep things fast and relevant, `toobig.py` automatically skips:

*   **Common Directories:** `.git`, `node_modules`, `venv`, `__pycache__`, `build`, `dist`, `target`, `.vscode`, `.idea`, `vendor`, `*.egg-info`, `.terraform`, and more.
*   **Non-Code File Extensions:** Images (`.png`, `.jpg`...), archives (`.zip`, `.tar`, `.gz`...), binaries (`.exe`, `.dll`, `.so`...), compiled code (`.pyc`, `.class`...), documents (`.pdf`, `.docx`...), media (`.mp4`, `.mp3`...), fonts, logs (`.log`), lock files (`.lock`), minified files (`.min.js`, `.min.css`), etc.

This focuses the analysis on the text-based files you're most likely to edit and refactor.

## 📊 Example Output

Running the script will give you something like this:

```plaintext
Analyzing repository in /path/to/your/project...
Excluding Dirs: ['.env', '.git', ..., 'vendor']
Excluding Exts: ['.7z', '.a', ..., '.zip']
Scanning: src/components                                          

Analysis Results:
Total number of files analyzed: 142
Total number of lines of text: 24510
Total number of characters: 910234

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
Size: 1.15 MB
Lines: 15000
Characters: 1200500
------------------------------------------------------------
```

Now go forth and refactor! ✂️
