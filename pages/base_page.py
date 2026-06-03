from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "") -> None:
        from config.env import BASE_URL
        self.page.goto(f"{BASE_URL}{path}")

    def wait_for_url(self, url_fragment: str) -> None:
        self.page.wait_for_url(f"**{url_fragment}**")

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(path=f"reports/screenshots/{name}.png", full_page=True)
