#!/usr/bin/env python3

import os
import sys

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
    """Count the lines and characters of a file."""
    num_lines = 0
    num_chars = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read line by line instead of all at once
            for line in f:
                num_lines += 1
                num_chars += len(line)
        return num_lines, num_chars
    except Exception as e:
        print(f"Unable to read file {file_path}: {e}")
        return 0, 0

def count_files_and_lines(directory):
    """Count the number of files, lines of text, and characters in a directory."""
    total_files = 0
    total_lines = 0
    total_chars = 0
    file_details = []
    processed_files = 0

    # Walk through all files in the directory
    for root, dirs, files in os.walk(directory):
        # Print progress: current directory being scanned
        # Use carriage return \r to overwrite the line
        progress_message = f"Scanning: {root}"
        # Pad with spaces to clear previous longer messages
        sys.stdout.write(f"\r{progress_message:<80}")
        sys.stdout.flush()

        # Exclude .git directory explicitly at the start
        if '.git' in dirs:
            dirs.remove('.git') # Don't descend into .git

        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is a text file (not binary)
            if is_text_file(file_path):
                total_files += 1
                num_lines, num_chars = count_file_details(file_path)
                total_lines += num_lines
                total_chars += num_chars
                file_size = os.path.getsize(file_path)
                file_details.append((file_path, file_size, num_lines, num_chars))
                processed_files += 1
                # Optional: Update progress more frequently, e.g., every 100 files
                # if processed_files % 100 == 0:
                #     sys.stdout.write(f"\rProcessed {processed_files} files...")
                #     sys.stdout.flush()


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
        print(f"Size: {file_size / 1024:.2f} KB")
        print(f"Lines: {num_lines}")
        print(f"Characters: {num_chars}")
        print('-' * 60)

def main():
    # Use the current directory (the root of the Git repository)
    local_dir = os.getcwd()

    # Analyze the repository in the current directory
    print(f"Analyzing repository in {local_dir}...")
    total_files, total_lines, total_chars, file_details = count_files_and_lines(local_dir)

    # Display the general results
    print(f"\nAnalysis Results:")
    print(f"Total number of files analyzed: {total_files}")
    print(f"Total number of lines of text: {total_lines}")
    print(f"Total number of characters: {total_chars}")

    # Display the largest files
    display_largest_files(file_details)

if __name__ == "__main__":
    main()
