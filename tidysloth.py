#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable

CATEGORIES = {
    "Code": {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp", ".h", ".hpp", ".go", ".rs", ".rb", ".php", ".sh", ".css", ".html", ".json", ".xml", ".yml", ".yaml", ".toml", ".md"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"},
    "Archives": {".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".tgz"},
}

INDEX_FILENAME = "TIDY_INDEX.md"


def categorize_file(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"


def iter_files(target_dir: Path) -> Iterable[Path]:
    category_dirs = set(CATEGORIES) | {"Others"}
    for path in sorted(target_dir.rglob("*")):
        if not path.is_file() or path.name == INDEX_FILENAME:
            continue
        try:
            relative = path.relative_to(target_dir)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] in category_dirs:
            continue
        yield path


def next_available_path(destination: Path) -> Path:
    if not destination.exists():
        return destination
    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def generate_index(target_dir: Path, categorized: dict[str, list[Path]], mode: str, dry_run: bool = False) -> Path:
    index_path = target_dir / INDEX_FILENAME
    lines = [
        "# TidySloth Index",
        "",
        f"- Mode: `{mode}`",
        f"- Dry run: `{dry_run}`",
        f"- Target: `{target_dir}`",
        "",
        "## Summary",
        "",
    ]

    total = 0
    for category in [*CATEGORIES.keys(), "Others"]:
        files = categorized.get(category, [])
        total += len(files)
        lines.append(f"- **{category}**: {len(files)}")

    lines.extend(["", f"**Total files scanned**: {total}", ""])

    for category in [*CATEGORIES.keys(), "Others"]:
        files = categorized.get(category, [])
        lines.append(f"## {category}")
        if not files:
            lines.append("- _(none)_")
        else:
            for file_path in files:
                try:
                    display = file_path.relative_to(target_dir)
                except ValueError:
                    display = file_path
                lines.append(f"- `{display}`")
        lines.append("")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


def scan_command(target_dir: Path) -> int:
    categorized: dict[str, list[Path]] = {category: [] for category in [*CATEGORIES.keys(), "Others"]}
    for file_path in iter_files(target_dir):
        categorized[categorize_file(file_path)].append(file_path)

    index_path = generate_index(target_dir, categorized, mode="scan")
    print(f"Scanned {target_dir}")
    print(f"Generated index: {index_path}")
    return 0


def tidy_command(target_dir: Path, dry_run: bool) -> int:
    categorized: dict[str, list[Path]] = {category: [] for category in [*CATEGORIES.keys(), "Others"]}

    for file_path in iter_files(target_dir):
        category = categorize_file(file_path)
        destination_dir = target_dir / category
        destination = next_available_path(destination_dir / file_path.name)
        categorized[category].append(destination)

        if dry_run:
            print(f"[DRY-RUN] {file_path} -> {destination}")
            continue

        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(destination))
        print(f"Moved {file_path} -> {destination}")

    index_path = generate_index(target_dir, categorized, mode="tidy", dry_run=dry_run)
    print(f"Generated index: {index_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TidySloth: organize files into category folders.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a directory and generate TIDY_INDEX.md")
    scan_parser.add_argument("target", nargs="?", default=".", help="Target directory to scan")

    tidy_parser = subparsers.add_parser("tidy", help="Organize files into category folders")
    tidy_parser.add_argument("target", nargs="?", default=".", help="Target directory to organize")
    tidy_parser.add_argument("--dry-run", action="store_true", help="Show intended changes without moving files")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = Path(args.target).expanduser().resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: target directory does not exist: {target_dir}")
        return 1

    if args.command == "scan":
        return scan_command(target_dir)
    if args.command == "tidy":
        return tidy_command(target_dir, dry_run=args.dry_run)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
