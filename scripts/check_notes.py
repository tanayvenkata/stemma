"""Fail when note links or SKILL.md references no longer resolve.

Run from anywhere: python3 scripts/check_notes.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "plugins" / "stemma" / "skills" / "stemma"
SKIP_DIRS = {".obsidian"}
ROOT_FILES = {"SKILL.md"}


def note_files():
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in SKIP_DIRS or str(relative) in ROOT_FILES:
            continue
        yield path


def main():
    problems = []
    by_name = defaultdict(list)
    notes = list(note_files())
    for path in notes:
        by_name[path.stem].append(path.relative_to(ROOT))

    for name, paths in by_name.items():
        if len(paths) > 1:
            problems.append(f"duplicate note name '{name}': {', '.join(map(str, paths))}")

    for path in notes:
        for target in re.findall(r"\[\[([^\]|#]+)", path.read_text(encoding="utf-8")):
            name = target.split("/")[-1].strip()
            if name not in by_name:
                problems.append(f"{path.relative_to(ROOT)}: broken link [[{target}]]")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for reference in sorted(set(re.findall(r"`([^`]+)`", skill))):
        if "<" in reference:
            continue
        if reference.endswith(".md"):
            if not (ROOT / reference).is_file():
                problems.append(f"SKILL.md: missing file `{reference}`")
        elif re.fullmatch(r"[A-Z][\w&,'@ -]+", reference) and reference not in by_name:
            problems.append(f"SKILL.md: no note named `{reference}`")

    for problem in problems:
        print(problem)
    print(f"{len(notes)} notes checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
