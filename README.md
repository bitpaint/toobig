# 🚀 TooBig: Find Your Chunky Files 🚀

Ever feel like your codebase is getting a bit... *chonky*? `toobig.py` is here to help you vibe check your project and spot those hefty files that might need a little refactoring love. ✨

It scans your current directory, counts up the text files, lines, and characters, and points out the biggest bois. Keep your code lean and mean! 💪

## 🤔 Why?

Big files can be a drag. They're harder to read, harder to maintain, and just generally mess with the coding flow. `toobig.py` helps you identify potential candidates for splitting into smaller, more manageable pieces. Keep it modular, keep it cool. 😎

## ✨ How to Use

It's super simple! Just curl the script directly from the repo and run it with Python in the root of your project directory:

```bash
curl -sSL https://raw.githubusercontent.com/bitpaint/toobig/main/toobig.py | python3
```

Alternatively, clone the repo and run it:
```bash
git clone https://github.com/bitpaint/toobig.git
cd toobig
python3 toobig.py
```

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