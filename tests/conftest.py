import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Keep pygame tests headless in CI/terminal environments.
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
