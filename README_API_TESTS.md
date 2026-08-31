# Automation Exercise — QA Practice

Automated tests against [automationexercise.com](https://automationexercise.com), a
public site built specifically for QA/automation practice, including a real
documented REST API.

## Project structure

```
automationexercise-qa/
├── tests/
│   └── test_products_api.py   # API tests (products, brands, search)
├── pytest.ini
└── requirements.txt
```

More coming: UI tests (Page Object Model) covering product data
completeness, cart & checkout eligibility, price/tier sanity, and search &
filter integrity — building on the API layer above.

## Why this project exists

A follow-up to [qa-playwright-practice](https://github.com/frangisondi/qa-playwright-practice),
this one adds **real API testing** (not UI mocking) since
automationexercise.com exposes a genuine, documented API
(`/api/productsList`, `/api/brandsList`, `/api/searchProduct`, etc.) —
letting these tests hit real endpoints and real responses directly.

## Setup

```bash
pip install -r requirements.txt
```

## Running the tests

```bash
pytest -v
```

Generates `report.html` — open it in a browser for a readable test report.

## Notes

- `test_search_returns_matching_products` originally assumed search only
  matches on product *name*. The first real run caught it returning a
  product filed under a matching *category* instead — a good example of a
  failing test flagging a wrong assumption in the test itself, not a bug
  in the app. The test was corrected to check both name and category.
