from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.error_message = page.locator('[data-test="error"]')
        self.summary_total = page.locator(".summary_total_label")
        self.order_complete_header = page.locator(".complete-header")

    def goto_info(self) -> None:
        self.navigate("/checkout-step-one.html")

    def fill_info(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    def get_total(self) -> str:
        return self.summary_total.inner_text()

    def expect_order_complete(self) -> None:
        expect(self.order_complete_header).to_have_text("Thank you for your order!")

    def expect_error(self, message: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(message)
