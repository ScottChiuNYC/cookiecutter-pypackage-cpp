"""Bootstrap this template's pinned development environment."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "template/scripts"))
from bootstrap import main

if __name__ == "__main__":
    main(ROOT / "template", ROOT / ".dev-tools")
