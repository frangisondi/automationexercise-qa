from playwright.sync_api import Page

BASE_URL = "https://automationexercise.com"


class CartPage:
    """Represents the shopping cart page."""

    URL = f"{BASE_URL}/view_cart"

    def __init__(self, page: Page):
        self.page = page
        self.cart_rows = page.locator("#cart_info_table tbody tr")

    def goto(self):
        self.page.goto(self.URL)

    def get_item_count(self) -> int:
        return self.cart_rows.count()

    def get_row_by_product_id(self, product_id: int):
        return self.page.locator(f"#product-{product_id}")

    def remove_item(self, product_id: int):
        self.page.locator(f"#product-{product_id} .cart_quantity_delete").click()

    def get_price_for_product(self, product_id: int) -> float:
        row = self.get_row_by_product_id(product_id)
        text = row.locator(".cart_price p").text_content()
        return float(text.replace("Rs.", "").strip())

    def get_total_for_product(self, product_id: int) -> float:
        row = self.get_row_by_product_id(product_id)
        text = row.locator(".cart_total .cart_total_price").text_content()
        return float(text.replace("Rs.", "").strip())

    def get_quantity_for_product(self, product_id: int) -> int:
        row = self.get_row_by_product_id(product_id)
        return int(row.locator(".cart_quantity button").text_content().strip())
