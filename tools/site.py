#!/usr/bin/env python3
"""Build or preview the Laplace-Wiki site.

  python3 tools/site.py build    # writes the site to site/
  python3 tools/site.py serve    # live preview at http://127.0.0.1:8000/

Needs the packages in tools/requirements.txt:
  python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    args = sys.argv[1:] or ["build"]
    # mkdocs.yml's docs_dir must exist before tools/site_hooks.py fills it.
    (ROOT / ".site-src").mkdir(exist_ok=True)
    venv = ROOT / ".venv" / ("Scripts" if os.name == "nt" else "bin") / "mkdocs"
    mkdocs = str(venv) if venv.exists() else shutil.which("mkdocs")
    if not mkdocs:
        sys.exit(__doc__)
    return subprocess.call([mkdocs, *args], cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
