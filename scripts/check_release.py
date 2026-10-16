"""Verify the exact reviewed payload. A manifest is not a privacy classifier."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".venv", "__pycache__", "demo_output"}


def main():
    manifest = json.loads((ROOT / "release-manifest.json").read_text())
    expected = manifest["sha256"]
    actual = set()
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            raise SystemExit(f"Symlink is not allowed in release: {rel}")
        if not path.is_file() or rel.as_posix() == "release-manifest.json":
            continue
        actual.add(rel.as_posix())
    if actual != set(expected):
        raise SystemExit(f"Payload differs: extra={sorted(actual-set(expected))}; missing={sorted(set(expected)-actual)}")
    for name, digest in expected.items():
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts:
            raise SystemExit("Invalid manifest path")
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != digest:
            raise SystemExit(f"File changed since review: {name}")
    print(f"PASS: {len(expected)} reviewed files match the release manifest.")


if __name__ == "__main__":
    main()
