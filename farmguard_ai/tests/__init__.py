# Tests package initialization
import sys
from pathlib import Path

# Automatically ensure project root is on sys.path for portable test execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
