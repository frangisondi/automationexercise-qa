"""
Price sanity, UI vs API. The API test file already confirms no product has
a $0/blank price in the raw data. This test goes one step further: it
confirms the price actually RENDERED on the product page matches what the
API (the real source of truth) says it should be. This catches a class of
bug the API test alone can't: correct data, but a rendering/caching bug
showing the wrong number to a real shopper.
"""

import pytest
import requests
from playwright.sync_api import Page

from pages.product_detail_page import ProductDetailPage

API_URL = "https://automationexercise.com/api/productsList"


def get_api_price(product_id: int) -> float:
    products = requests.get(API_URL).json()["products"]
    match = next(p for p in products if p["id"] == product_id)
    return float(match["price"].replace("Rs.", "").strip())


class TestPriceTierSanity:
    @pytest.mark.parametrize("product_id", [1, 2, 3, 6, 33])
    def test_storefront_price_matches_api_price(self, page: Page, product_id: int):
        detail_page = ProductDetailPage(page)
        detail_page.goto(product_id)

        # Page price text looks like "Rs. 500"
        raw_ui_price = detail_page.price.text_content()
        ui_price = float(raw_ui_price.replace("Rs.", "").strip())

        api_price = get_api_price(product_id)

        assert ui_price == api_price, (
            f"Product {product_id}: storefront shows Rs. {ui_price}, "
            f"API says Rs. {api_price} — storefront/API mismatch"
        )

    @pytest.mark.parametrize("product_id", [1, 2, 3, 6, 33])
    def test_no_zero_or_blank_price_on_storefront(self, page: Page, product_id: int):
        detail_page = ProductDetailPage(page)
        detail_page.goto(product_id)

        raw_price = detail_page.price.text_content()
        assert raw_price.strip() != "", f"Product {product_id} has a blank price"

        value = float(raw_price.replace("Rs.", "").strip())
        assert value > 0, f"Product {product_id} shows a price of Rs. {value}"
