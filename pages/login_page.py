from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def goto(self) -> None:
        self.navigate()

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_error(self, message: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(message)

    def expect_logged_in(self) -> None:
        self.wait_for_url("/inventory.html")
