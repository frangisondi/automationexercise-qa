"""
Cart & checkout eligibility — drives the storefront like a real shopper:
add items, confirm the cart reflects them correctly (quantity, price,
total), and confirm removing an item updates the cart correctly.

Deliberately stops at the cart page and does not proceed into a real
account signup/checkout/payment flow.
"""

from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage

BACKPACK_ID = 1  # "Blue Top", Rs. 500
SECOND_ITEM_ID = 2  # "Men Tshirt", Rs. 400


class TestCartCheckoutEligibility:
    def test_add_single_item_reflects_correct_price_and_quantity(self, page: Page):
        products_page = ProductsPage(page)
        products_page.goto()
        products_page.add_to_cart_by_product_id(BACKPACK_ID)
        products_page.close_added_to_cart_modal()

        cart_page = CartPage(page)
        cart_page.goto()

        assert cart_page.get_item_count() == 1
        assert cart_page.get_quantity_for_product(BACKPACK_ID) == 1
        assert cart_page.get_price_for_product(BACKPACK_ID) == 500.0
        assert cart_page.get_total_for_product(BACKPACK_ID) == 500.0

    def test_add_multiple_items_cart_shows_each_correctly(self, page: Page):
        products_page = ProductsPage(page)
        products_page.goto()
        products_page.add_to_cart_by_product_id(BACKPACK_ID)
        products_page.close_added_to_cart_modal()
        products_page.add_to_cart_by_product_id(SECOND_ITEM_ID)
        products_page.close_added_to_cart_modal()

        cart_page = CartPage(page)
        cart_page.goto()

        assert cart_page.get_item_count() == 2
        assert cart_page.get_price_for_product(BACKPACK_ID) == 500.0
        assert cart_page.get_price_for_product(SECOND_ITEM_ID) == 400.0

    def test_remove_item_updates_cart(self, page: Page):
        products_page = ProductsPage(page)
        products_page.goto()
        products_page.add_to_cart_by_product_id(BACKPACK_ID)
        products_page.close_added_to_cart_modal()

        cart_page = CartPage(page)
        cart_page.goto()
        assert cart_page.get_item_count() == 1

        cart_page.remove_item(BACKPACK_ID)
        expect(cart_page.get_row_by_product_id(BACKPACK_ID)).to_have_count(0)
