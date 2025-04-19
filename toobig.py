#!/usr/bin/env python3

import os
import sys
import fnmatch
import argparse

# --- Constants ---
DEFAULT_EXCLUDED_DIRS = {
    # Version Control & Config
    '.git', '.hg', '.svn',
    # IDE/Editor
    '.vscode', '.idea', '.vs',
    # Language Specific Artifacts
    '__pycache__', '*.pyc', '*.pyo', '*.egg-info', '*.class', '*.jar', '*.war', '*.ear', '.gradle',
    'target', # Java/Scala/Rust
    'node_modules', 'bower_components', '.npm', '.yarn',
    'vendor', # Go/PHP/Ruby
    '_build', # Elixir/Erlang
    'deps', # Elixir/Erlang
    'build', 'dist', 'out', # General build outputs
    # Virtual Environments
    'venv', '.venv', 'env', '.env',
    # OS Specific
    '.DS_Store', 'Thumbs.db',
    # Terraform
    '.terraform',
    # Other common build/cache
    'buck-out', '.metals', '.bloop', 'site-packages',
    '.next', '.nuxt',
    # Lock Files (add specific filenames here)
    'package-lock.json', 'yarn.lock', 'composer.lock', 'Gemfile.lock', 'Pipfile.lock', 'poetry.lock',
    'mix.lock', # Elixir lock file
}

DEFAULT_EXCLUDED_EXTENSIONS = {
    # Common Binary/Non-code formats
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.ico', '.webp', '.svg',
    '.zip', '.tar', '.gz', '.rar', '.7z', '.tgz',
    '.exe', '.dll', '.so', '.o', '.a', '.lib', '.dylib', '.app', '.obj', '.bin',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp',
    '.sqlite', '.db', '.mdb', '.log', '.lock',
    '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac', '.ogg', '.mkv',
    '.woff', '.woff2', '.eot', '.ttf', '.otf',
    # Minified files (often large but not primary source)
    '.min.js', '.min.css',
    # Data files
    '.csv', '.tsv', '.sql',
    # Notebooks
    '.ipynb',
}

# Box drawing characters
TL, TR, BL, BR, H, V, LC, RC = '┌', '┐', '└', '┘', '─', '│', '├', '┤'

# --- Helper Functions ---

def parse_gitignore(gitignore_path):
    """Parses a .gitignore file and returns a list of patterns."""
    patterns = []
    if not os.path.exists(gitignore_path):
        return patterns
    try:
        with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Basic handling: treat as fnmatch pattern
                    # Doesn't handle negation (!) or complex path rules perfectly
                    patterns.append(line)
    except Exception as e:
        print(f"\nWarning: Could not read or parse .gitignore: {e}", file=sys.stderr)
    return patterns

def format_size(size_bytes):
    """Formats size in bytes to KB or MB."""
    size_kb = size_bytes / 1024
    if size_kb >= 1024:
        return f"{size_kb / 1024:.2f} MB"
    else:
        return f"{size_kb:.2f} KB"

def print_boxed_title(title, width=80):
    """Prints a centered title within a box."""
    print(f"{TL}{H * (width - 2)}{TR}")
    print(f"{V}{title.center(width - 2)}{V}")
    print(f"{LC}{H * (width - 2)}{RC}")


# --- Core Logic ---

def count_file_details(file_path):
    """Count the lines and characters of a file.

    Returns:
        tuple: (num_lines, num_chars) or (0, 0) if unable to read.
    """
    num_lines = 0
    num_chars = 0
    try:
        # Try UTF-8 first, common for code
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                num_lines += 1
                num_chars += len(line)
        return num_lines, num_chars
    except UnicodeDecodeError:
        # If UTF-8 fails, try default encoding (often latin-1 or cp1252 on Windows)
        # Use errors='ignore' as a fallback for potentially mixed/binary content
        try:
            with open(file_path, 'r', encoding=sys.getdefaultencoding(), errors='ignore') as f:
                 for line in f:
                    num_lines += 1
                    num_chars += len(line)
            return num_lines, num_chars
        except Exception as e:
            # print(f"Unable to read file {file_path} with fallback encoding: {e}") # Optional debug
            return 0, 0 # Indicate failure if fallback also errors
    except Exception as e:
        # print(f"Unable to read file {file_path}: {e}") # Optional debug
        return 0, 0 # Indicate failure

def count_files_and_lines(directory, excluded_dirs, excluded_extensions, gitignore_patterns, verbose=False):
    """Count relevant files, lines, and chars, respecting exclusions and .gitignore."""
    total_files = 0
    total_lines = 0
    total_chars = 0
    file_details = []
    start_dir = os.path.abspath(directory)
    width = 80 # For progress message padding

    # Pre-compile gitignore patterns for efficiency if needed (simple fnmatch doesn't need it)

    for root, dirs, files in os.walk(directory, topdown=True):
        abs_root = os.path.abspath(root)
        rel_root = os.path.relpath(abs_root, start_dir)
        if rel_root == '.':
            rel_root = '' # Root directory relative path is empty

        # --- Filtering Directories ---
        original_dirs = list(dirs)
        dirs[:] = [] # Clear dirs and selectively add back allowed ones
        for d in original_dirs:
            abs_dir_path = os.path.join(abs_root, d)
            rel_dir_path = os.path.join(rel_root, d).replace('\\', '/') # Use forward slashes for matching

            # 1. Check hardcoded excluded dir names/patterns
            if any(fnmatch.fnmatch(d, pattern) for pattern in excluded_dirs):
                continue

            # 2. Check .gitignore patterns (match against relative path)
            is_gitignored = False
            for pattern in gitignore_patterns:
                # Match directory itself or pattern ending with /
                if fnmatch.fnmatch(rel_dir_path, pattern) or \
                   (pattern.endswith('/') and fnmatch.fnmatch(rel_dir_path, pattern.rstrip('/'))):
                   is_gitignored = True
                   break
            if is_gitignored:
                continue

            # If not excluded, add back to dirs for os.walk to descend
            dirs.append(d)

        # --- Progress Update ---
        progress_message = f"⏳ Scanning: {rel_root or '.'}" # Added hourglass
        sys.stdout.write(f"\r{progress_message:<{width}}")
        sys.stdout.flush()

        # --- Filtering Files ---
        for file in files:
            abs_file_path = os.path.join(abs_root, file)
            rel_file_path = os.path.join(rel_root, file).replace('\\', '/') # Use forward slashes
            _, ext = os.path.splitext(file)

            # 1. Check hardcoded excluded filenames/patterns (like package-lock.json)
            if any(fnmatch.fnmatch(file, pattern) for pattern in excluded_dirs):
                continue

            # 2. Check hardcoded excluded extensions
            if ext.lower() in excluded_extensions:
                continue

            # 3. Check .gitignore patterns (match against relative path)
            is_gitignored = False
            for pattern in gitignore_patterns:
                if fnmatch.fnmatch(rel_file_path, pattern):
                    is_gitignored = True
                    break
            if is_gitignored:
                continue

            # --- Process File ---
            try:
                file_size = os.path.getsize(abs_file_path)
                num_lines, num_chars = count_file_details(abs_file_path)

                # Check if reading failed but file has size (likely binary/unreadable)
                if num_lines == 0 and num_chars == 0 and file_size > 0:
                    if verbose:
                        # Clear progress line before printing skip message
                        sys.stdout.write(f"\r{' ':<{width}}\r")
                        print(f"❓ Skipping likely binary/unreadable: {rel_file_path}") # Added question mark emoji
                        # Reprint progress line
                        sys.stdout.write(f"\r{progress_message:<{width}}")
                        sys.stdout.flush()
                    continue

                # Count valid text files (including empty ones)
                total_files += 1
                total_lines += num_lines
                total_chars += num_chars
                file_details.append((rel_file_path, file_size, num_lines, num_chars))

            except OSError:
                # Ignore files that might disappear during scan or have permission issues
                continue

    # Clear the progress line before printing results
    sys.stdout.write(f"\r{' ':<{width}}\r")
    sys.stdout.flush()
    return total_files, total_lines, total_chars, file_details

def display_largest_files(file_details, top_n=5, width=80):
    """Display the top 'n' largest files in a formatted box."""
    if not file_details:
        no_files_text = "🤔 No files found matching criteria."
        print(f"{V}{no_files_text:<{width - 2}}{V}")
        return

    # Correct alignment for top files header
    top_files_title = f"🏆 Top {top_n} Largest Files by Size 🏆"
    print(f"{V}{top_files_title.center(width - 2)}{V}")
    print(f"{LC}{H * (width - 2)}{RC}")

    # Sort the files by size, from largest to smallest
    sorted_files = sorted(file_details, key=lambda x: x[1], reverse=True)[:top_n]

    for idx, (file_path, file_size, num_lines, num_chars) in enumerate(sorted_files, start=1):
        size_str = format_size(file_size)
        # Add file emoji
        line1 = f" #{idx} 📁 {file_path}"
        line2 = f"    Size: {size_str} | Lines: {num_lines} | Chars: {num_chars}"

        print(f"{V}{line1:<{width - 2}}{V}")
        print(f"{V}{line2:<{width - 2}}{V}")
        if idx < len(sorted_files):
             print(f"{LC}{H * (width - 2)}{RC}") # Separator


# --- Main Execution ---

ASCII_ART = [
    "  ┌┬┐┌─┐┌─┐  ┌┐ ┬┌─┐",
    "   │ │ ││ │  ├┴┐││ ┬",
    "   ┴ └─┘└─┘  └─┘┴└─┘"
]

def main():
    parser = argparse.ArgumentParser(
        description="Find the largest text files in a directory, respecting .gitignore.",
        formatter_class=argparse.RawTextHelpFormatter, # Keep formatting in help
        epilog='''\ 
Examples:
  python toobig.py                 # Scan current dir, show top 5
  python toobig.py --top 10 ./src  # Scan ./src, show top 10
  python toobig.py --exclude-exts .log,.tmp -v # Exclude more, be verbose

Using with curl:
  curl -sSL .../toobig.py | python3 -- --top 10
'''
    )
    parser.add_argument(
        'directory', nargs='?', default=os.getcwd(),
        help="Directory to analyze (default: current directory)"
    )
    parser.add_argument(
        '--top', type=int, default=5,
        help="Number of largest files to display (default: 5)"
    )
    parser.add_argument(
        '--exclude-dirs', type=str, default='',
        help="Comma-separated list of additional directory patterns to exclude (fnmatch)"
    )
    parser.add_argument(
        '--exclude-exts', type=str, default='',
        help="Comma-separated list of additional file extensions (e.g., .log,.tmp)"
    )
    parser.add_argument(
        '--no-gitignore', action='store_true',
        help="Do not read or respect .gitignore files"
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="Show potentially binary/unreadable files that are skipped"
    )

    args = parser.parse_args()
    width = 80 # Define output width

    # --- ASCII Art Banner ---
    print() # Add newline before banner
    for line in ASCII_ART:
        print(line.center(width)) # Center the art
    # Add the repository link underneath, also centered
    repo_link = "https://github.com/bitpaint/toobig"
    print(repo_link.center(width))
    print() # Add newline after banner + link

    # --- Title --- 
    print_boxed_title("🚀 File Analyzer 🚀", width=width)

    # --- Setup Exclusions --- 
    excluded_dirs = DEFAULT_EXCLUDED_DIRS.copy()
    if args.exclude_dirs:
        excluded_dirs.update(d.strip() for d in args.exclude_dirs.split(',') if d.strip())

    excluded_extensions = DEFAULT_EXCLUDED_EXTENSIONS.copy()
    if args.exclude_exts:
        exts = {('.' + e.strip()) if not e.strip().startswith('.') else e.strip()
                for e in args.exclude_exts.split(',') if e.strip()}
        excluded_extensions.update(exts)

    gitignore_patterns = []
    if not args.no_gitignore:
        gitignore_path = os.path.join(args.directory, '.gitignore')
        gitignore_patterns = parse_gitignore(gitignore_path)
        # print(f"Debug: Found {len(gitignore_patterns)} patterns in .gitignore")

    target_dir = args.directory
    top_n = args.top

    if not os.path.isdir(target_dir):
        print(f"{V} Error: Directory not found: {target_dir} {V}".ljust(width - 1) + V, file=sys.stderr)
        print(f"{BL}{H * (width - 2)}{BR}", file=sys.stderr)
        sys.exit(1)

    # --- Run Analysis --- 
    try:
        abs_target_dir = os.path.abspath(target_dir)
        # Ensure path doesn't overflow the box
        max_path_len = width - 19 # Account for text, emoji, borders
        display_path = abs_target_dir
        if len(display_path) > max_path_len:
            display_path = "..." + display_path[-(max_path_len - 3):]

        # Correct alignment for info section
        analyze_text = f" 🔍 Analyzing: {display_path}"
        print(f"{V}{analyze_text:<{width - 2}}{V}")
        ignore_text = f"   Ignoring .gitignore: {'Yes' if args.no_gitignore else 'No'}"
        print(f"{V}{ignore_text:<{width - 2}}{V}")
        print(f"{LC}{H * (width - 2)}{RC}")

        total_files, total_lines, total_chars, file_details = count_files_and_lines(
            target_dir, excluded_dirs, excluded_extensions, gitignore_patterns, args.verbose
        )

        # --- Display Results --- 
        # Correct alignment for results header
        results_title = "📊 Analysis Results 📊"
        print(f"{V}{results_title.center(width - 2)}{V}")
        print(f"{LC}{H * (width - 2)}{RC}")
        results_line1 = f" 📄 Files Analyzed: {total_files}"
        results_line2 = f" 📏 Total Lines: {total_lines}"
        results_line3 = f" 🔠 Total Chars: {total_chars}"
        print(f"{V}{results_line1:<{width - 2}}{V}")
        print(f"{V}{results_line2:<{width - 2}}{V}")
        print(f"{V}{results_line3:<{width - 2}}{V}")
        print(f"{LC}{H * (width - 2)}{RC}")

        display_largest_files(file_details, top_n=top_n, width=width)

        print(f"{BL}{H * (width - 2)}{BR}") # Footer for the whole output
        print() # Add newline after output

    except KeyboardInterrupt:
        # Clear any leftover progress line
        sys.stdout.write(f"\r{' ':<{width}}\r")
        sys.stdout.flush()
        # Add emoji to interrupt message
        print(f"\n{V} 🛑 Scan interrupted by user. {V}".center(width + 1), file=sys.stderr)
        print(f"{BL}{H * (width - 2)}{BR}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Clear any leftover progress line
        sys.stdout.write(f"\r{' ':<{width}}\r")
        sys.stdout.flush()
        # Add emoji to error message
        print(f"\n{V} ⚠️ An unexpected error occurred: {e} {V}".ljust(width -1) + V, file=sys.stderr)
        print(f"{BL}{H * (width - 2)}{BR}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
