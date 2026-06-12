import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.env import HEADLESS, SLOW_MO, TIMEOUT, BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage


# ---------------------------------------------------------------------------
# Session-scoped: one browser instance for the whole test run
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_instance(request):
    # 1. Fetch the value from the CLI
    browser_input = request.config.getoption("--browser", default="chromium")

    # 2. Safely extract the string if it's a list, fallback if it's empty
    if isinstance(browser_input, list):
        if browser_input:
            browser_name = browser_input[0]
        else:
            browser_name = "chromium"  # Fallback if list is empty []
    else:
        browser_name = browser_input or "chromium"  # Fallback if None/empty string

    # 3. Spin up Playwright
    with sync_playwright() as pw:
        if browser_name == "firefox":
            browser_type = pw.firefox
        elif browser_name == "webkit":
            browser_type = pw.webkit
        else:
            browser_type = pw.chromium

        browser = browser_type.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Session-scoped: perform login once, save storage state for reuse
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def authenticated_context(browser_instance: Browser):
    """
    Log in once per session and reuse the browser storage state.
    Avoids repeating the login UI flow in every test — much faster at scale.
    """
    context = browser_instance.new_context(base_url=BASE_URL)
    context.set_default_timeout(TIMEOUT)
    page = context.new_page()

    login = LoginPage(page)
    login.goto()
    login.login(STANDARD_USER, PASSWORD)
    login.expect_logged_in()

    # Persist cookies + localStorage so subsequent contexts can restore instantly
    storage = context.storage_state()
    context.close()

    yield storage


# ---------------------------------------------------------------------------
# Function-scoped: fresh page per test, but with pre-authenticated state
# ---------------------------------------------------------------------------

@pytest.fixture
def auth_page(browser_instance: Browser, authenticated_context: dict) -> Page:
    """
    Each test gets a clean page that starts already logged in.
    Isolation: tests don't share page state or cart contents.
    """
    context = browser_instance.new_context(
        base_url=BASE_URL,
        storage_state=authenticated_context,
    )
    context.set_default_timeout(TIMEOUT)
    page = context.new_page()
    yield page
    context.close()


# ---------------------------------------------------------------------------
# Function-scoped: unauthenticated page for login/error tests
# ---------------------------------------------------------------------------

@pytest.fixture
def page(browser_instance: Browser) -> Page:
    context = browser_instance.new_context(base_url=BASE_URL)
    context.set_default_timeout(TIMEOUT)
    page = context.new_page()
    yield page
    context.close()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot on test failure and attach to the report."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page: Page | None = item.funcargs.get("auth_page") or item.funcargs.get("page")
        if page:
            import os
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_path = f"reports/screenshots/{item.nodeid.replace('/', '_').replace('::', '__')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            # Attach to Allure report if available
            try:
                import allure
                allure.attach.file(
                    screenshot_path,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except ImportError:
                pass
