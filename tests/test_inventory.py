import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage


@pytest.mark.inventory
class TestInventory:
    def test_inventory_page_loads(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.expect_on_page()

    def test_all_six_products_displayed(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        items = inventory.get_item_names()
        assert len(items) == 6

    def test_sort_by_price_low_to_high(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.sort_by("lohi")

        prices = auth_page.locator(".inventory_item_price").all_inner_texts()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric), "Products not sorted low-to-high"

    def test_sort_by_price_high_to_low(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.sort_by("hilo")

        prices = auth_page.locator(".inventory_item_price").all_inner_texts()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric, reverse=True), "Products not sorted high-to-low"

    def test_sort_alphabetically_a_to_z(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.sort_by("az")

        names = inventory.get_item_names()
        assert names == sorted(names), "Products not sorted A-Z"

    def test_add_item_updates_cart_badge(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()

        assert inventory.get_cart_count() == 0
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

    def test_add_multiple_items_updates_cart_count(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()

        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.add_item_to_cart("sauce-labs-bike-light")
        assert inventory.get_cart_count() == 2

    def test_remove_item_updates_cart_badge(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()

        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

        inventory.remove_item_from_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 0
