"""
UI version of "data completeness" — checks each product's real detail page
renders every field a shopper needs to make a decision. This complements
(doesn't duplicate) the API version: the API test checks the DATA is valid,
this checks the PAGE actually RENDERS it correctly to a real user.
"""

import pytest
from playwright.sync_api import Page

from pages.product_detail_page import ProductDetailPage

# A representative sample across categories, not all ~34 products — keeps
# the test suite fast while still covering each product type. In a real
# job, you'd weigh "test everything" against "tests need to run often and
# stay fast" — this is that tradeoff in practice.
SAMPLE_PRODUCT_IDS = [1, 2, 3, 6, 33, 39]  # top, tshirt, dress, top, jeans, saree


class TestDataCompleteness:
    @pytest.mark.parametrize("product_id", SAMPLE_PRODUCT_IDS)
    def test_product_detail_page_is_complete(self, page: Page, product_id: int):
        detail_page = ProductDetailPage(page)
        detail_page.goto(product_id)

        missing_fields = detail_page.is_complete()
        assert not missing_fields, (
            f"Product {product_id} is missing: {missing_fields}"
        )

    def test_no_duplicate_product_names_on_listing(self, page: Page):
        """UI-level duplicate check, mirroring the API version — catches
        the case where the API data is fine but a rendering bug duplicates
        a card on the page itself."""
        page.goto("https://automationexercise.com/products")
        names = page.locator(".product-image-wrapper .productinfo p").all_text_contents()

        duplicates = {name for name in names if names.count(name) > 1}
        assert not duplicates, f"Duplicate products rendered on page: {duplicates}"
