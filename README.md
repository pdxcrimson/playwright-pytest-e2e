# playwright-pytest-e2e

[![E2E Tests](https://github.com/pdxcrimson/playwright-pytest-e2e/actions/workflows/e2e.yml/badge.svg)](https://github.com/pdxcrimson/playwright-pytest-e2e/actions)

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

This project uses **uv** for extremely fast dependency management and Python version control. You do not need to have a specific Python version pre-installed — `uv` will handle it for you.

### Install uv

- **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Install Allure CLI

Allure is a Java-based reporting tool installed separately from the Python dependencies.

**Linux / WSL2:**
```bash
sudo apt update && sudo apt install -y default-jre
wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure_2.29.0-1_all.deb
sudo dpkg -i allure_2.29.0-1_all.deb
```

**macOS:**
```bash
brew install allure
```

**Windows:**
```bash
scoop install allure
```

> **Linux/WSL2 shortcut:** Run `./setup.sh` after cloning — it handles Java, Allure, browsers, and Python dependencies in one step.

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pdxcrimson/playwright-pytest-e2e.git
   cd playwright-pytest-e2e
   ```

2. **Initialize the environment**:
   ```bash
   uv sync
   ```
   This creates a `.venv`, installs Python >=3.10, and syncs all dependencies (playwright, pytest, faker, etc.).

3. **Install Playwright browsers**:
   ```bash
   uv run playwright install chromium firefox
   ```

4. **Linux / WSL2 only — install browser system dependencies**:
   ```bash
   sudo uv run playwright install-deps chromium
   ```

---

## Running tests

```bash
# Full suite
uv run pytest

# Specific test file
uv run pytest tests/test_auth.py -v

# Specific marker
uv run pytest -m auth
uv run pytest -m checkout

# Single browser
uv run pytest --browser=chromium
uv run pytest --browser=firefox

# Multiple browsers
uv run pytest --browser=chromium --browser=firefox

# Parallel (auto-detect workers)
uv run pytest -n auto

# Headed mode (watch the browser — not supported in WSL2 without a display)
HEADLESS=false uv run pytest -m smoke

# Generate Allure results
uv run pytest --alluredir=reports/allure-results

# Serve the Allure report (opens in browser)
allure serve reports/allure-results
Note: allure not supported on WSL2 at this time; support will be added later.
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
├── setup.sh            # One-step setup for Linux / WSL2
└── .github/workflows/  # CI: lint → test (Chromium + Firefox) → Allure report
```

---

## CI/CD

The GitHub Actions workflow runs on every push and PR:

1. **Lint** — black, flake8, isort
2. **E2E** — runs in parallel across Chromium and Firefox
3. **Report** — merges Allure results and publishes to GitHub Pages

Test artifacts (screenshots, HTML reports) are retained for 30 days.

---

## Tech stack

| Tool | Purpose |
|------|---------|
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [Pytest](https://pytest.org) | Test runner + fixtures |
| [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) | Parallel test execution |
| [Allure](https://allurereport.org) | Interactive HTML test reporting |
| [Faker](https://faker.readthedocs.io) | Test data generation |
| [uv](https://docs.astral.sh/uv/) | Fast Python package manager |
| [pre-commit](https://pre-commit.com) | Code quality hooks (black, flake8, isort) |
