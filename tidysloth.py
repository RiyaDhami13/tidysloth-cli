#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Define standard extension mapping for local categorization
EXTENSION_MAP = {
    "Code": [".py", ".js", ".ts", ".cpp", ".c", ".html", ".css", ".json", ".sh"],
    "Documents": [".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx", ".pptx"],
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"]
}

def get_category(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    for category, extensions in EXTENSION_MAP.items():
        if suffix in extensions:
            return category
    return "Others"

def scan_directory(target_dir: Path) -> dict:
    """Scans directory and groups files by intended category without moving them."""
    summary = {cat: [] for cat in list(EXTENSION_MAP.keys()) + ["Others"]}
    
    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist.")
        return summary

    for item in target_dir.iterdir():
        if item.is_file() and item.name != "TIDY_INDEX.md":
            cat = get_category(item)
            summary[cat].append(item.name)
            
    return summary

def tidy_directory(target_dir: Path, dry_run: bool = False) -> None:
    """Organizes files into categorized subfolders and generates a summary markdown file."""
    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist.")
        return

    summary = scan_directory(target_dir)
    total_moved = 0

    print(f"\n🦥 TidySloth scanning '{target_dir}'...")
    
    for category, files in summary.items():
        if not files:
            continue
            
        cat_folder = target_dir / category
        if not dry_run and files:
            cat_folder.mkdir(exist_ok=True)
            
        for file_name in files:
            src = target_dir / file_name
            dest = cat_folder / file_name
            
            if dry_run:
                print(f"[DRY RUN] Would move: {file_name} -> {category}/")
            else:
                shutil.move(str(src), str(dest))
                print(f"Moved: {file_name} -> {category}/")
                total_moved += 1

    # Generate Markdown Index Summary
    generate_index(target_dir, summary)
    print(f"\n✨ Done! Organized {total_moved} files safely at local speed.")

def generate_index(target_dir: Path, summary: dict) -> None:
    index_path = target_dir / "TIDY_INDEX.md"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = [
        "# 🦥 TidySloth Organization Index",
        f"*Generated on: {date_str}*",
        "",
        "> *" + "Organized locally with zero cloud uploads. Stay slow, stay steady." + "*",
        ""
    ]
    
    for category, files in summary.items():
        lines.append(f"## 📁 {category} ({len(files)} files)")
        if files:
            for f in files:
                lines.append(f"- `{f}`")
        else:
            lines.append("- *No files in this category*")
        lines.append("")
        
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"📄 Generated index manifest at {index_path}")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TidySloth CLI: Clean up digital clutter locally.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Preview how files will be categorized")
    scan_parser.add_argument("--path", type=str, default=".", help="Target directory to scan")

    # Tidy command
    tidy_parser = subparsers.add_parser("tidy", help="Organize files and generate index")
    tidy_parser.add_argument("--path", type=str, default=".", help="Target directory to tidy")
    tidy_parser.add_argument("--dry-run", action="store_true", help="Preview moves without changing files")

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    target = Path(args.path).resolve()

    if args.command == "scan":
        print(f"\n🔍 Scanning folder: {target}")
        summary = scan_directory(target)
        for cat, files in summary.items():
            print(f"[{cat}] -> {len(files)} files: {files}")
            
    elif args.command == "tidy":
        tidy_directory(target, dry_run=args.dry_run)

if __name__ == "__main__":
    main()