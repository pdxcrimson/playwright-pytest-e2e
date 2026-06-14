import json
import os
from pathlib import Path
from playwright.sync_api import Page


def load_test_data(filename: str) -> dict:
    """Load JSON test data from config/test_data/."""
    path = Path(__file__).parent.parent / "config" / "test_data" / filename
    with open(path) as f:
        return json.load(f)


def get_storage_state_path() -> str:
    """Return path for saved browser auth state."""
    os.makedirs("reports", exist_ok=True)
    return "reports/auth_state.json"


def save_storage_state(page: Page) -> None:
    """Persist browser storage state (cookies + localStorage) to disk."""
    state_path = get_storage_state_path()
    page.context.storage_state(path=state_path)


def assert_url_contains(page: Page, fragment: str) -> None:
    assert fragment in page.url, f"Expected URL to contain '{fragment}', got: {page.url}"
