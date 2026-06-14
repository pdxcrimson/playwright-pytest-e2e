import pytest
from playwright.sync_api import Page

from config.env import LOCKED_USER, PASSWORD, STANDARD_USER
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.auth
class TestLogin:
    def test_standard_user_can_login(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.login(STANDARD_USER, PASSWORD)
        login.expect_logged_in()

    def test_locked_user_sees_error(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.login(LOCKED_USER, PASSWORD)
        login.expect_error("Sorry, this user has been locked out")

    def test_invalid_credentials_show_error(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.login("not_a_user", "wrong_password")
        login.expect_error("Username and password do not match")

    def test_empty_username_shows_error(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.login("", PASSWORD)
        login.expect_error("Username is required")

    def test_empty_password_shows_error(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.login(STANDARD_USER, "")
        login.expect_error("Password is required")


@pytest.mark.auth
class TestLogout:
    def test_user_can_logout(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()

        auth_page.locator("#react-burger-menu-btn").click()
        auth_page.locator('[data-test="logout-sidebar-link"]').click()

        # Should be back on login page
        assert "saucedemo.com" in auth_page.url
        assert "inventory" not in auth_page.url
