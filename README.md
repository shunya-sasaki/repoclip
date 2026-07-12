# Repoclip

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&labelColor=gray&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?logo=uv&labelColor=gray&logoColor=white)

`repoclip` is a small command-line tool that reads the source files in a
repository and copies their combined contents to your system clipboard. It is
handy for pasting a whole project (or a subset of it) into an LLM chat or a
document, with each file clearly delimited by its path.

## 📦 Requirements

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) (recommended for installation)

## ⚙️ Setup

```sh
uv tool install git+https://github.com/shunya-sasaki/repoclip.git
```

## 🚀 Usage

Run `repoclip` inside a repository to copy the contents of every supported
file to the clipboard:

```sh
repoclip
```

You can also point it at a specific directory or a single file:

```sh
repoclip path/to/dir
repoclip path/to/file.py
```

Pass `--verbose` to print a table of the character count per file:

```sh
repoclip --verbose
```

### How it works

- When the target is a directory, files are collected recursively.
- Only files with the following suffixes are included:
  `.c`, `.cc`, `.conf`, `.cpp`, `.h`, `.js`, `.json`, `.jsonc`, `.jsx`, `.md`,
  `.py`, `.toml`, `.ts`, `.tsx`, `.txt`, `.vue`.
- Paths matching `.venv/*`, `.git/*`, `*.pyc`, `*/__pycache__`, or `*.lock`
  are skipped.
- Each file is emitted with its path as a header, separated by dividers.
- If the combined output exceeds 128,000 characters, a warning is printed.

### Example

Given a small project:

```text
myproject/
├── README.md
└── src/
    └── main.py
```

Running `repoclip` from the project root:

```sh
$ repoclip --verbose
Copied contents (412 chars).
 Char counts for each
        file
┏━━━━━━━━━━━━━┳━━━━━━━┓
┃ Path        ┃ Chars ┃
┡━━━━━━━━━━━━━╇━━━━━━━┩
│ README.md   │    31 │
│ src/main.py │    32 │
└─────────────┴───────┘
```

The clipboard now holds each file wrapped with its path:

```text
--------------------------------------------------------------------------------
README.md
--------------------------------------------------------------------------------
# Sample

A tiny demo project.


--------------------------------------------------------------------------------
src/main.py
--------------------------------------------------------------------------------
def add(a, b):
    return a + b
```

## 📄 License

MIT License

See [LICENSE](./LICENSE) for the detail
