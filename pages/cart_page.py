from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping = page.locator('[data-test="continue-shopping"]')
        self.cart_items = page.locator(".cart_item")

    def goto(self) -> None:
        self.navigate("/cart.html")

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def remove_item(self, item_name: str) -> None:
        slug = item_name.lower().replace(" ", "-")
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def expect_item_present(self, item_name: str) -> None:
        expect(self.page.locator(".inventory_item_name", has_text=item_name)).to_be_visible()

    def expect_empty(self) -> None:
        expect(self.cart_items).to_have_count(0)
