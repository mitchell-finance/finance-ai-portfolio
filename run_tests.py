"""Run all demo suites in isolated interpreters (some examples share module names)."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CHILD = """
import unittest, sys
suite = unittest.defaultTestLoader.discover(".")
count = suite.countTestCases()
if not count:
    sys.exit("Empty test suite")
result = unittest.TextTestRunner(stream=sys.stderr).run(suite)
if not result.wasSuccessful():
    sys.exit(1)
print(count)
"""

def main():
    total = 0
    folders = sorted(p for p in (ROOT / "demos").iterdir() if p.is_dir() and not p.name.startswith("."))
    for folder in folders:
        result = subprocess.run([sys.executable, "-c", CHILD], cwd=folder,
                                stdout=subprocess.PIPE, text=True)
        if result.returncode:
            sys.exit(f"Failed suite: {folder.name}")
        count = int(result.stdout.strip())
        print(f"{folder.name}: {count} passed", flush=True)
        total += count
    if not total:
        sys.exit("No demo tests discovered")
    print(f"{total} tests passed across {len(folders)} demos.")

if __name__ == "__main__":
    main()
