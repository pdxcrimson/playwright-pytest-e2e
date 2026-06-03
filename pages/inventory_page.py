from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')

    def goto(self) -> None:
        self.navigate("/inventory.html")

    def add_item_to_cart(self, item_name: str) -> None:
        slug = item_name.lower().replace(" ", "-")
        self.page.locator(f'[data-test="add-to-cart-{slug}"]').click()

    def remove_item_from_cart(self, item_name: str) -> None:
        slug = item_name.lower().replace(" ", "-")
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def sort_by(self, option: str) -> None:
        self.sort_dropdown.select_option(option)

    def go_to_cart(self) -> None:
        self.cart_icon.click()

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_item_price(self, item_name: str) -> float:
        slug = item_name.lower().replace(" ", "-")
        price_text = self.page.locator(f'[data-test="inventory-item-{slug}-price"]').inner_text()
        return float(price_text.replace("$", ""))

    def expect_on_page(self) -> None:
        expect(self.page_title).to_have_text("Products")
