# Automation Exercise — QA Practice

Automated tests against [automationexercise.com](https://automationexercise.com), a
public site built specifically for QA/automation practice, including a real
documented REST API.

## Project structure

```
automationexercise-qa/
├── pages/                          # Page Object classes (UI tests)
│   ├── products_page.py
│   ├── product_detail_page.py
│   └── cart_page.py
├── tests/
│   ├── test_products_api.py        # API tests (products, brands, search)
│   ├── test_data_completeness.py   # UI: product detail pages fully render
│   ├── test_price_tier_sanity.py   # UI: storefront price vs API price
│   ├── test_cart_checkout.py       # UI: add/remove cart eligibility
│   └── test_search_filter.py       # UI: category, brand, and search results
├── postman/                        # Manual/exploratory API testing
│   ├── Automation_Exercise_API.postman_collection.json
│   └── README.md
├── .github/workflows/tests.yml     # CI: runs the full suite on every push
├── pytest.ini
└── requirements.txt
```

## Why this project exists

A follow-up to [qa-playwright-practice](https://github.com/frangisondi/qa-playwright-practice),
this one goes further in two directions:

1. **Real API testing** — automationexercise.com exposes a genuine,
   documented API (`/api/productsList`, `/api/brandsList`,
   `/api/searchProduct`, `/api/verifyLogin`), so these tests hit real
   endpoints directly instead of mocking, plus a **Postman collection**
   for manual/exploratory testing of the same endpoints.
2. **A richer UI surface** — this site has real search, filters,
   categories, and brands (saucedemo didn't), enabling tests that weren't
   possible before: search/filter integrity, and a storefront-vs-API price
   cross-check that catches rendering bugs the API alone can't see.

## Setup

```bash
pip install -r requirements.txt
playwright install
```

## Running the tests

```bash
pytest -v --headed
```

Generates `report.html` — open it in a browser for a readable test report.

### CI

Every push to `main` runs the full suite automatically via GitHub Actions
(see `.github/workflows/tests.yml`).

### Postman

See `postman/README.md` for the manual/exploratory API testing collection —
same endpoints as `test_products_api.py`, different testing approach.

## Notes — real bugs and mistakes caught along the way

- `test_search_returns_matching_products` originally assumed search only
  matches on product *name*. The first real run caught it returning a
  product filed under a matching *category* instead — a good example of a
  failing test flagging a wrong assumption in the test itself, not a bug
  in the app. The test was corrected to check both name and category.
- The cart tests initially failed on first run (`assert 0 == 1`) — not a
  wrong selector, but a real timing/race condition: the code navigated to
  the cart page before the "item added" confirmation had actually finished,
  so the cart appeared empty. Fixed by waiting for that confirmation to
  appear before continuing.
- The Postman collection's "Brand List" test was initially copy-pasted from
  "Product List" and checked for the wrong shape of data entirely (product
  fields on a brand response). Fixed to check the fields this endpoint
  actually returns.
