"""pytest configuration and fixtures for the test suite."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to Python path so tools module can be imported
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
