# Postman Collection

Manual/exploratory API testing companion to the automated `pytest` suite in
this repo. Same target (automationexercise.com's real API), two different
testing approaches:

- **Postman** (this folder) — request-by-request exploration, useful for
  manually checking behavior, debugging a specific endpoint, or documenting
  expected request/response shape for someone new to the API.
- **pytest** (`../tests/test_products_api.py`) — full automated regression
  suite, meant to run unattended (e.g. in CI) and catch breakage over time.

## Requests included

| Request | Method | What it checks |
|---|---|---|
| Product List | GET | Every product includes name, price, and brand |
| Brand List | GET | Every brand has an id and a name |
| Search Products | POST | Search returns at least one relevant result |
| Verify Email | POST | An unregistered email correctly returns a 404 |

## How to use

1. Open Postman → Import → select `Automation_Exercise_API.postman_collection.json`
2. Click into any request → Send
3. Check the **Test Results** tab (next to Body/Cookies) for pass/fail

## Note

The exported collection initially had a copy-paste bug — the "Brand List"
request was checking for product-shaped data (`name`/`price`/`brand` on a
product object) instead of brand-shaped data. This version has the corrected
assertion. A good reminder that copy-pasting a working test onto a new
endpoint still needs a real read-through, not just a re-run.
