import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils.factories import make_checkout_info


@pytest.mark.checkout
class TestCheckout:
    @pytest.fixture(autouse=True)
    def add_item_to_cart(self, auth_page: Page):
        """Add a product before each checkout test."""
        inventory = InventoryPage(auth_page)
        inventory.goto()
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(auth_page)
        cart.proceed_to_checkout()

    def test_complete_checkout_happy_path(self, auth_page: Page):
        info = make_checkout_info()
        checkout = CheckoutPage(auth_page)
        checkout.fill_info(info.first_name, info.last_name, info.postal_code)
        checkout.finish()
        checkout.expect_order_complete()

    def test_checkout_shows_order_total(self, auth_page: Page):
        info = make_checkout_info()
        checkout = CheckoutPage(auth_page)
        checkout.fill_info(info.first_name, info.last_name, info.postal_code)

        total = checkout.get_total()
        assert "$" in total, f"Expected a dollar amount in total, got: {total}"

    def test_missing_first_name_shows_error(self, auth_page: Page):
        checkout = CheckoutPage(auth_page)
        checkout.fill_info("", "Smith", "98101")
        checkout.expect_error("First Name is required")

    def test_missing_last_name_shows_error(self, auth_page: Page):
        checkout = CheckoutPage(auth_page)
        checkout.fill_info("Jane", "", "98101")
        checkout.expect_error("Last Name is required")

    def test_missing_postal_code_shows_error(self, auth_page: Page):
        checkout = CheckoutPage(auth_page)
        checkout.fill_info("Jane", "Smith", "")
        checkout.expect_error("Postal Code is required")


@pytest.mark.checkout
@pytest.mark.parametrize(
    "first,last,postal,expected_error",
    [
        ("", "Smith", "98101", "First Name is required"),
        ("Jane", "", "98101", "Last Name is required"),
        ("Jane", "Smith", "", "Postal Code is required"),
    ],
)
def test_checkout_form_validation(auth_page: Page, first, last, postal, expected_error):
    """Data-driven validation — demonstrates pytest.mark.parametrize."""
    inventory = InventoryPage(auth_page)
    inventory.goto()
    inventory.add_item_to_cart("sauce-labs-backpack")
    inventory.go_to_cart()

    CartPage(auth_page).proceed_to_checkout()
    checkout = CheckoutPage(auth_page)
    checkout.fill_info(first, last, postal)
    checkout.expect_error(expected_error)
