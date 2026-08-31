from playwright.sync_api import Page

BASE_URL = "https://automationexercise.com"


class ProductDetailPage:
    """Represents a single product's detail page: /product_details/{id}."""

    def __init__(self, page: Page):
        self.page = page
        self.product_image = page.locator(".view-product img")
        self.name = page.locator(".product-information h2")
        self.category = page.locator(".product-information p:has-text('Category:')")
        self.price = page.locator(".product-information span span")
        self.availability = page.locator(".product-information p:has-text('Availability:')")
        self.condition = page.locator(".product-information p:has-text('Condition:')")
        self.brand = page.locator(".product-information p:has-text('Brand:')")

    def goto(self, product_id: int):
        self.page.goto(f"{BASE_URL}/product_details/{product_id}")

    def is_complete(self) -> list[str]:
        """
        Checks every expected field is present and non-empty. Returns a
        list of missing/empty field names (empty list = fully complete).
        """
        missing = []
        if not self.product_image.is_visible():
            missing.append("image")
        if not self.name.text_content().strip():
            missing.append("name")
        if not self.category.text_content().strip():
            missing.append("category")
        if not self.price.text_content().strip():
            missing.append("price")
        if not self.availability.text_content().strip():
            missing.append("availability")
        if not self.condition.text_content().strip():
            missing.append("condition")
        if not self.brand.text_content().strip():
            missing.append("brand")
        return missing
