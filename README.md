# tidysloth-cli

A local-first Python file-organizer CLI that cleans up digital clutter at sloth speed.

## Features

- Organizes files into category folders: `Code`, `Documents`, `Images`, `Archives`, and `Others`
- Uses `pathlib` for path handling and `argparse` for CLI parsing
- Supports a non-destructive preview mode with `--dry-run`
- Generates a markdown summary index (`TIDY_INDEX.md`) for both scan and tidy runs

## Requirements

- Python 3.9+

## Usage

Run from this repository root:

```bash
python tidysloth.py --help
```

### Scan a directory

Scans files and writes `TIDY_INDEX.md` with category counts and file listings.

```bash
python tidysloth.py scan /path/to/target
```

If no target is provided, the current directory is used:

```bash
python tidysloth.py scan
```

### Tidy a directory

Moves files into category subfolders and updates `TIDY_INDEX.md`.

```bash
python tidysloth.py tidy /path/to/target
```

### Dry run

Preview all move operations without changing any files:

```bash
python tidysloth.py tidy /path/to/target --dry-run
```

## File categorization

- **Code**: common source/config/markup extensions (for example `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.md`)
- **Documents**: office/text data (for example `.pdf`, `.docx`, `.txt`, `.csv`)
- **Images**: common image formats (for example `.png`, `.jpg`, `.svg`)
- **Archives**: compressed bundles (for example `.zip`, `.tar`, `.gz`, `.7z`)
- **Others**: everything else

## Notes

- Existing files already under category folders are skipped.
- Name conflicts are handled by appending a numeric suffix (for example `report_1.pdf`).
- `TIDY_INDEX.md` is not moved during tidy operations.
