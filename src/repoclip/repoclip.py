"""Repoclip main module."""

from fnmatch import fnmatch
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from typer import Argument
from typer import Option

from repoclip.utils import Clipboard


class CountTable(Table):
    """Rich table summarizing character counts per file."""

    def __init__(self, title: str, dict_count: dict[str, int]):
        """Initialize the table.

        Args:
            title: Title displayed above the table.
            dict_count: Mapping of file path to its character count.
        """
        super().__init__(title=title)
        self.add_column("Path", justify="left")
        self.add_column("Chars", justify="right")
        for k, v in dict_count.items():
            self.add_row(k, f"{v:,}")


class Repoclip:
    """Read contents of files in a repo and copy to the system clipboard."""

    TARGET_SUFFIXES = [
        ".c",
        ".cc",
        ".conf",
        ".cpp",
        ".h",
        ".js",
        ".json",
        ".jsonc",
        ".jsx",
        ".md",
        ".py",
        ".toml",
        ".ts",
        ".tsx",
        ".txt",
        ".vue",
    ]

    EXCLUDE_PATTERN = [".venv/*", ".git/*", "*.pyc", "*/__pycache__", "*.lock"]
    MAX_CHARS = 128000

    def __init__(self):
        """Initializer of Repoclip."""
        self.app = typer.Typer()
        self.app.command(
            help="Read files in current repository and copy the contents"
            + " to the system clipboard."
        )(self.repo2clip)

    def repo2clip(
        self,
        path: Annotated[str, Argument(help="Target path")] = ".",
        verbose: Annotated[bool, Option(is_flag=True)] = False,
    ):
        """Read target files and copy their contents to the clipboard.

        When ``path`` is a directory, every file whose suffix is in
        ``TARGET_SUFFIXES`` is collected recursively, skipping paths that
        match ``EXCLUDE_PATTERN``. When ``path`` is a single file, only that
        file is read. The concatenated contents are copied to the system
        clipboard, and a warning is printed if the total length exceeds
        ``MAX_CHARS``.

        Args:
            path: Target file or directory to read. Defaults to the current
                directory.
            verbose: If True, print a table of character counts per file.
        """
        target_path = Path(path)
        if target_path.is_dir():
            target_filepathes = [
                p
                for p in target_path.glob("**/*")
                if (p.is_file()) and p.suffix in self.TARGET_SUFFIXES
            ]
        else:
            target_filepathes = [target_path]
        dict_count = {}
        outputs = []
        for target_filepath in target_filepathes:
            is_exclude = any(
                fnmatch(target_filepath.as_posix(), pattern)
                for pattern in self.EXCLUDE_PATTERN
            )
            if is_exclude:
                continue
            name = target_filepath.as_posix()
            try:
                contents = target_filepath.read_text()
            except UnicodeDecodeError:
                contents = target_filepath.read_text(encoding="utf-8")
            outputs.append(
                "-" * 80
                + "\n"
                + name
                + "\n"
                + "-" * 80
                + "\n"
                + contents
                + "\n"
            )
            dict_count[name] = len(contents)
        output = "\n".join(outputs)
        Clipboard.copy(output)
        console = Console()
        console.print(f"Copied contents ({len(output)} chars).")
        if len(output) > self.MAX_CHARS:
            console.print(
                f"⚠️ Number of chars exceeds the limit {self.MAX_CHARS}!",
                style="bold yellow",
            )
        if verbose:
            table = CountTable(
                title="Char voutns for each file", dict_count=dict_count
            )
            console.print(table)


def run():
    """Entry point of Repoclip."""
    clip = Repoclip()
    clip.app()
