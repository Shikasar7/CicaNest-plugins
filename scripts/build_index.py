"""Build the market list: each folder in plugins/ zipped into dist/<id>-<version>.zip, and index.json
(format 1, what nest's plugin market reads) listing them with their sha256 and size.

Usage: python scripts/build_index.py [--base https://raw.githubusercontent.com/<owner>/CicaNest-plugins/main]

Each zip holds the plugin's folder as it is (plugin.json at the top). The zip is made the same way every
time (sorted names, fixed times), so an unchanged plugin keeps its sha256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE = "https://raw.githubusercontent.com/Shikasar7/CicaNest-plugins/main"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
KIND_TRUST = {"python": "trusted", "mcp": "code", "skills": "guides", "companion": "guides"}
TRUST_ORDER = ("content", "guides", "code", "trusted")


def trust_of(kinds: list[str]) -> str:
    levels = [KIND_TRUST.get(k, "content") for k in kinds] or ["content"]
    return max(levels, key=TRUST_ORDER.index)


def build_zip(folder: Path, target: Path) -> bytes:
    target.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in folder.rglob("*") if p.is_file())
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(folder).as_posix(), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return target.read_bytes()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE, help="where the repository's files are served from")
    base = parser.parse_args().base.rstrip("/")
    entries = []
    for folder in sorted(p for p in (ROOT / "plugins").iterdir() if p.is_dir()):
        manifest = json.loads((folder / "plugin.json").read_text(encoding="utf-8"))
        kinds = sorted((manifest.get("provides") or {}).keys())
        name = f"{manifest['id']}-{manifest['version']}.zip"
        data = build_zip(folder, ROOT / "dist" / name)
        asked = manifest.get("permissions") or {}
        entries.append(
            {
                "id": manifest["id"],
                "name": manifest["name"],
                "version": manifest["version"],
                "author": manifest.get("author", ""),
                "description": manifest.get("description", ""),
                "kinds": kinds,
                "trust": trust_of(kinds),
                "url": f"{base}/dist/{name}",
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
                "permissions": {
                    "network": asked.get("network") or [],
                    "secrets": [s.get("name", s) if isinstance(s, dict) else s for s in asked.get("secrets") or []],
                    "confirm": asked.get("confirm") or [],
                },
            }
        )
    index = {"format": 1, "plugins": entries}
    (ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"index.json: {len(entries)} 个插件")


if __name__ == "__main__":
    main()
