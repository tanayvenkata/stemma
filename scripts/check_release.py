"""Fail when the plugin version, the marketplace entry, and the changelog disagree.

plugin.json holds the only version number. Installed copies update only when it
changes, so each release bumps it and adds a matching CHANGELOG.md heading.

Run from anywhere: python3 scripts/check_release.py
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "stemma" / ".claude-plugin" / "plugin.json"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
CHANGELOG = REPO / "CHANGELOG.md"


def main():
    problems = []
    plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
    version = plugin.get("version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        problems.append(f"plugin.json version '{version}' is not MAJOR.MINOR.PATCH")

    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    entries = [p for p in marketplace.get("plugins", []) if p.get("name") == plugin.get("name")]
    if len(entries) != 1:
        problems.append(f"marketplace.json should list '{plugin.get('name')}' exactly once")
    elif "version" in entries[0]:
        problems.append("marketplace.json entry sets a version; keep it only in plugin.json")

    headings = re.findall(r"^## (\d+\.\d+\.\d+)\b", CHANGELOG.read_text(encoding="utf-8"), re.M)
    if not headings or headings[0] != version:
        latest = headings[0] if headings else "none"
        problems.append(f"latest CHANGELOG.md entry is {latest}, plugin.json is {version}")

    for problem in problems:
        print(problem)
    print(f"version {version}: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
