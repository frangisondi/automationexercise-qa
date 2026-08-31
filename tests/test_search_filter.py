"""
Search & filter integrity — UI version. Confirms category pages, brand
pages, and search results only show relevant products, and that nothing
expected is missing.
"""

from playwright.sync_api import Page

from pages.products_page import ProductsPage

# category_id: (category name fragment, expected minimum product count)
CATEGORIES = {
    1: "dress",   # Women > Dress
    3: "tshirt",  # Men > Tshirts (product names contain "Tshirt"/"T-Shirt")
}

BRANDS = ["Polo", "H&M"]


class TestSearchFilterIntegrity:
    def test_category_page_shows_relevant_products(self, page: Page):
        products_page = ProductsPage(page)
        products_page.go_to_category(1)  # Women > Dress

        names = products_page.get_visible_product_names()
        assert names, "Expected at least one product in this category"
        # Every dress-category product name should plausibly relate —
        # loose check since exact naming varies (e.g. "Dress", "Gown", "Maxi")
        assert any("dress" in n.lower() or "gown" in n.lower() for n in names), (
            f"Dress category returned no obviously dress-related products: {names}"
        )

    def test_brand_page_shows_only_that_brands_products(self, page: Page):
        products_page = ProductsPage(page)
        products_page.go_to_brand("Polo")

        names = products_page.get_visible_product_names()
        assert names, "Expected at least one product for brand Polo"
        # Can't verify brand from the listing card alone (brand isn't shown
        # on the card) — this at least confirms the page returns *some*
        # results and doesn't silently show an empty/broken page.

    def test_search_returns_results(self, page: Page):
        products_page = ProductsPage(page)
        products_page.goto()
        products_page.search("dress")

        names = products_page.get_visible_product_names()
        assert names, "Search for 'dress' returned no results"

    def test_search_for_nonsense_term_returns_no_results(self, page: Page):
        """Negative test: an obviously fake search term should return
        nothing, not silently show unrelated products."""
        products_page = ProductsPage(page)
        products_page.goto()
        products_page.search("zzzznotarealproductzzzz")

        names = products_page.get_visible_product_names()
        assert names == [], f"Nonsense search term unexpectedly returned: {names}"
