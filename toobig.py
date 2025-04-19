#!/usr/bin/env python3

import os
import sys
import fnmatch
import argparse # Add argparse for command-line arguments

# Directories common in various projects that should be excluded (default set)
DEFAULT_EXCLUDED_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', 'env', '.env',
    '__pycache__', 'build', 'dist', 'target', '.vscode', '.idea',
    '*.egg-info', '.metals', '.bloop', 'site-packages', 'deps',
    '_build', 'buck-out', '.next', '.nuxt', 'out', '.terraform',
    'vendor' # Added common vendor dirs
}

# File extensions typically representing non-source code (default set)
DEFAULT_EXCLUDED_EXTENSIONS = {
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.ico', '.webp', '.svg',
    # Archives
    '.zip', '.tar', '.gz', '.rar', '.7z', '.tgz',
    # Binary/Executables
    '.exe', '.dll', '.so', '.o', '.a', '.lib', '.dylib', '.app',
    # Compiled Code / Intermediates
    '.class', '.pyc', '.jar', '.war', '.ear', '.obj', '.bin',
    # Documents / Data Formats (often large or binary)
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp',
    '.sqlite', '.db', '.mdb', '.log', # Moved log here
    # Media
    '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac', '.ogg', '.mkv',
    # Fonts
    '.woff', '.woff2', '.eot', '.ttf', '.otf',
    # Other
    '.lock', '.DS_Store', '.min.js', '.min.css' # Exclude minified files
}

def is_excluded(path, root):
    """Check if a file or directory should be excluded based on configured patterns."""
    rel_path = os.path.relpath(path, root)
    path_parts = rel_path.split(os.sep)

    # Check directory patterns
    for part in path_parts[:-1]: # Check parent directories
        if any(fnmatch.fnmatch(part, pattern) for pattern in EXCLUDED_DIRS):
            return True

    # Check file extension
    _, ext = os.path.splitext(path)
    if ext.lower() in EXCLUDED_EXTENSIONS:
        return True

    # Check filename itself for exclusion patterns (like *.egg-info which acts like a dir)
    filename = path_parts[-1]
    if any(fnmatch.fnmatch(filename, pattern) for pattern in EXCLUDED_DIRS):
         return True # Handle cases like *.egg-info treated as files/dirs

    return False

def is_text_file(file_path):
    """Determine if a file is a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Try reading the start of the file to check if it contains text
            f.read(1024)
        return True
    except (UnicodeDecodeError, IOError):
        return False

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

def count_files_and_lines(directory, excluded_dirs, excluded_extensions, verbose=False):
    """Count the number of relevant files, lines of text, and characters in a directory."""
    total_files = 0
    total_lines = 0
    total_chars = 0
    file_details = []
    processed_files = 0
    start_dir = directory # Remember the starting directory for exclusion checks

    # Walk through all files in the directory
    for root, dirs, files in os.walk(directory, topdown=True):
        # --- Filtering ---
        # Filter directories in-place to prevent descending into them
        original_dirs = list(dirs) # Copy before modifying
        # Use the passed-in exclusion set
        dirs[:] = [d for d in original_dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in excluded_dirs)]

        # Print progress: current directory being scanned
        progress_message = f"Scanning: {os.path.relpath(root, start_dir)}"
        sys.stdout.write(f"\r{progress_message:<80}")
        sys.stdout.flush()

        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            # --- Exclusion Check ---
            # Check extension first (quick)
            if ext.lower() in excluded_extensions: # Use the passed-in exclusion set
                continue

            # --- Process File ---
            # We attempt to count details, assuming it *might* be text.
            # count_file_details handles errors gracefully if it's binary.
            num_lines, num_chars = count_file_details(file_path)
            # Only count files that could be successfully read (num_lines > 0 or num_chars > 0 implies success)
            # Or count files that are 0 bytes (empty files are valid)
            if num_lines > 0 or num_chars > 0 or os.path.getsize(file_path) == 0:
                 if num_lines == 0 and num_chars == 0 and os.path.getsize(file_path) > 0:
                     # If reading failed (returned 0,0) but size > 0, likely binary - skip.
                     if verbose:
                         print(f"\rSkipping likely binary/unreadable file: {file_path:<70}")
                     continue

                 total_files += 1
                 total_lines += num_lines
                 total_chars += num_chars
                 file_size = os.path.getsize(file_path) # Get size directly
                 file_details.append((file_path, file_size, num_lines, num_chars))
                 processed_files += 1


    # Clear the progress line before printing results
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()
    return total_files, total_lines, total_chars, file_details

def display_largest_files(file_details, top_n=5):
    """Display the top 'n' largest files with their line and character counts."""
    # Sort the files by size, from largest to smallest
    sorted_files = sorted(file_details, key=lambda x: x[1], reverse=True)[:top_n]

    print(f"Top {top_n} Largest Files:")
    print('-' * 60)

    for idx, (file_path, file_size, num_lines, num_chars) in enumerate(sorted_files, start=1):
        print(f"#{idx} {file_path}")
        # Format size nicely (KB or MB)
        size_kb = file_size / 1024
        if size_kb > 1024:
            print(f"Size: {size_kb / 1024:.2f} MB")
        else:
            print(f"Size: {size_kb:.2f} KB")
        print(f"Lines: {num_lines}")
        print(f"Characters: {num_chars}")
        print('-' * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze code file sizes in a directory, excluding common non-code files/dirs.",
        epilog="Example: python toobig.py --top 10 --exclude-exts .log,.tmp --exclude-dirs my_data_dir"
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
        help="Comma-separated list of additional directory patterns to exclude"
    )
    parser.add_argument(
        '--exclude-exts', type=str, default='',
        help="Comma-separated list of additional file extensions (starting with '.') to exclude"
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="Show potentially binary/unreadable files that are skipped"
    )

    args = parser.parse_args()

    # Combine default and user-provided exclusions
    excluded_dirs = DEFAULT_EXCLUDED_DIRS.copy()
    if args.exclude_dirs:
        excluded_dirs.update(d.strip() for d in args.exclude_dirs.split(',') if d.strip())

    excluded_extensions = DEFAULT_EXCLUDED_EXTENSIONS.copy()
    if args.exclude_exts:
        # Ensure extensions start with a dot
        exts = {e.strip() if e.strip().startswith('.') else '.' + e.strip()
                for e in args.exclude_exts.split(',') if e.strip()}
        excluded_extensions.update(exts)

    target_dir = args.directory
    top_n = args.top

    if not os.path.isdir(target_dir):
        print(f"Error: Directory not found: {target_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Analyzing repository in {os.path.abspath(target_dir)}...")
        print(f"Excluding Dirs: {sorted(list(excluded_dirs))}")
        print(f"Excluding Exts: {sorted(list(excluded_extensions))}")
        total_files, total_lines, total_chars, file_details = count_files_and_lines(
            target_dir, excluded_dirs, excluded_extensions, args.verbose
        )

        # Display the general results
        print(f"\nAnalysis Results:")
        print(f"Total number of files analyzed: {total_files}")
        print(f"Total number of lines of text: {total_lines}")
        print(f"Total number of characters: {total_chars}")

        # Display the largest files
        display_largest_files(file_details, top_n=top_n)

    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
