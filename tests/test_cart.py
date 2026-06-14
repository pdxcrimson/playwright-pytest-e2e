import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.cart
class TestCart:
    def test_added_item_appears_in_cart(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(auth_page)
        cart.expect_item_present("Sauce Labs Backpack")

    def test_multiple_items_in_cart(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.add_item_to_cart("sauce-labs-bike-light")
        inventory.go_to_cart()

        cart = CartPage(auth_page)
        assert cart.get_item_count() == 2

    def test_remove_item_from_cart(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(auth_page)
        cart.remove_item("sauce-labs-backpack")
        cart.expect_empty()

    def test_continue_shopping_returns_to_inventory(self, auth_page: Page):
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.go_to_cart()

        cart = CartPage(auth_page)
        cart.continue_shopping.click()
        inventory.expect_on_page()
