# playwright-pytest-e2e

[![E2E Tests](https://github.com/yourusername/playwright-pytest-e2e/actions/workflows/e2e.yml/badge.svg)](https://github.com/yourusername/playwright-pytest-e2e/actions)

End-to-end test suite for [SauceDemo](https://www.saucedemo.com) built with Playwright + Pytest. Demonstrates production-grade SDET practices: Page Object Model, session-scoped auth fixtures, data-driven tests, parallel execution, and Allure reporting.

---

## Architecture decisions

**Why session-scoped auth?**
Logging in via the UI for every test is slow and tests the wrong thing. `conftest.py` performs login once per session, saves the browser storage state (cookies + localStorage), and injects it into each test's context. Tests stay fast and focused on their own behavior.

**Why a test data factory?**
Static fixtures (hardcoded names, postal codes) mask bugs where input format matters. `utils/factories.py` uses `faker` to generate realistic, unique data per run — catching edge cases that `"John Smith, 12345"` never would.

**Why `api_client` alongside UI tests?**
For tests that need preconditions (e.g. items in a cart), hitting the API directly to set up state is 10–50× faster than driving the UI. UI tests should test UI behavior, not re-test setup flows.

---

## Prerequisites

This project uses **uv** for extremely fast dependency management and Python version control. You do not need to have a specific Python version pre-installed; `uv` will handle it for you.

### Install uv
- **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

## Installation & Setup

1. **Clone the repository**:
   ```
   git clone https://github.com/pdxcrimson/playwright-pytest-e2e.git
   cd playwright-pytest-e2e
2. **Initialize the environment**:
   ```uv sync```
   
_This command creates a `.venv`, installs Python >=3.10, and syncs all dependencies (playwright, pytest, faker, etc.) to your local machine._

---

## Running tests

```bash
# Full suite
pytest

# Specific marker
pytest -m auth
pytest -m checkout

# Single browser
pytest --browser=firefox

# Parallel (4 workers)
pytest -n 4

# Headed (watch the browser)
HEADLESS=false pytest -m smoke

# With Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Project structure

```
├── pages/              # Page Object Model — one class per page
│   ├── base_page.py    # Shared navigation + helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/              # Test modules, one per feature area
│   ├── test_auth.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── utils/
│   ├── factories.py    # Faker-based test data generation
│   └── helpers.py      # Shared utilities
├── config/
│   ├── env.py          # Environment config via os.getenv
│   └── test_data/      # Static JSON fixtures
├── conftest.py         # Pytest fixtures: browser, auth session, screenshot hook
├── pytest.ini          # Markers, log config, test path
└── .github/workflows/  # CI: lint → test (3 browsers, parallel) → Allure report
```

---

## CI/CD

The GitHub Actions workflow runs on every push and PR:
1. **Lint** — black, flake8, isort
2. **E2E** — runs in parallel across Chromium, Firefox, and WebKit
3. **Report** — merges Allure results and publishes to GitHub Pages

Test artifacts (screenshots, HTML reports) are retained for 30 days.

---

## Tech stack

| Tool | Purpose |
|------|---------|
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [Pytest](https://pytest.org) | Test runner + fixtures |
| [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) | Parallel test execution |
| [Allure](https://allurereport.org) | HTML test reporting |
| [Faker](https://faker.readthedocs.io) | Test data generation |
| [pre-commit](https://pre-commit.com) | Code quality hooks |
