from playwright.sync_api import Page

BASE_URL = "https://automationexercise.com"


class ProductsPage:
    """Represents the 'All Products' listing page and category/brand pages."""

    URL = f"{BASE_URL}/products"

    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_header = page.locator("h2.title.text-center")
        self.product_cards = page.locator(".product-image-wrapper")

    def goto(self):
        self.page.goto(self.URL)

    def search(self, term: str):
        self.search_input.fill(term)
        self.search_button.click()

    def go_to_category(self, category_id: int):
        self.page.goto(f"{BASE_URL}/category_products/{category_id}")

    def go_to_brand(self, brand_name: str):
        self.page.goto(f"{BASE_URL}/brand_products/{brand_name}")

    def get_visible_product_names(self) -> list[str]:
        return self.product_cards.locator(".productinfo p").all_text_contents()

    def add_to_cart_by_product_id(self, product_id: int):
        """
        Each product card has an "Add to cart" link tied to a specific
        product ID. This clicks that specific one rather than "the first
        button on the page," so it works reliably across different pages.
        """
        self.page.locator(
            f"a[data-product-id='{product_id}'], "
            f"a.add-to-cart[data-product-id='{product_id}']"
        ).first.click()

    def close_added_to_cart_modal(self):
        """
        The 'Added!' popup needs to be dismissed to keep browsing. We wait
        for it to actually appear before clicking — without this wait, the
        code can race ahead to the cart page before the add-to-cart request
        has actually finished, making the cart look empty (a real timing
        bug caught on first run, not a wrong selector).
        """
        continue_button = self.page.locator("button:has-text('Continue Shopping')")
        continue_button.wait_for(state="visible", timeout=5000)
        continue_button.click()
