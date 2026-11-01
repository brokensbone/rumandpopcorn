"""Compare Hugo URL exports and rendered paths before/after a content change.

Run `hugo list all > before.csv` on the base revision and again as after.csv
on the changed revision. Pass both CSVs and clean production build directories.
New pages are allowed; existing source URLs and output files must remain.
"""

import csv
from pathlib import Path
import sys


def source_urls(filename):
    with Path(filename).open(newline="") as stream:
        return {
            row["path"]: row["permalink"]
            for row in csv.DictReader(stream)
            if row["path"]
        }


def output_paths(directory):
    root = Path(directory)
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


if len(sys.argv) != 5:
    raise SystemExit(
        "Usage: check_content_urls.py before.csv after.csv before-public after-public"
    )

before = source_urls(sys.argv[1])
after = source_urls(sys.argv[2])
old_files = output_paths(sys.argv[3])
new_files = output_paths(sys.argv[4])
if not before or not after or not old_files or not new_files:
    raise SystemExit("URL exports and build directories must be nonempty")

errors = [
    f"{path}: {url} -> {after.get(path, 'MISSING')}"
    for path, url in before.items()
    if after.get(path) != url
]
errors.extend(f"Missing output: {path}" for path in sorted(old_files - new_files))
if errors:
    raise SystemExit("\n".join(errors))
print(f"Preserved {len(before)} source URLs and {len(old_files)} rendered files.")
