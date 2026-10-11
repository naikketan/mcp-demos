import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVERS_DIR = REPO_ROOT / "servers"


def _load_expenses_module():
    """Load the hyphenated expenses-tracker-server.py as an importable module."""
    module_path = SERVERS_DIR / "expenses-tracker-server.py"
    spec = importlib.util.spec_from_file_location("expenses_tracker_server", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["expenses_tracker_server"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def expenses_server():
    """Fresh expenses-tracker server module with cleared in-memory state."""
    module = _load_expenses_module()
    module.EXPENSES.clear()
    return module
