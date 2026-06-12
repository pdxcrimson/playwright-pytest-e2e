# Contributing

## Adding a test

1. Write the page interaction in `pages/` if it doesn't exist yet.
2. Add the test in the appropriate `tests/test_*.py` file.
3. Tag it with the right marker (`@pytest.mark.auth`, etc.).
4. Run `pytest -m your_marker` to verify locally.

## Adding a page object

- Inherit from `BasePage`.
- Declare all locators in `__init__` — never hardcode selectors in test files.
- Prefer `data-test` attributes; fall back to ARIA roles.
- Methods should describe *user intent* (`login()`, `add_item_to_cart()`), not DOM actions (`click_button()`).

## Pre-commit

All commits run black, flake8, and isort automatically. Run manually:
```bash
pre-commit run --all-files
```

## Markers

| Marker | When to use |
|--------|------------|
| `@pytest.mark.smoke` | Critical path — runs on every deploy |
| `@pytest.mark.auth` | Login/logout flows |
| `@pytest.mark.inventory` | Product listing and sorting |
| `@pytest.mark.cart` | Cart add/remove behavior |
| `@pytest.mark.checkout` | Checkout form and order completion |
| `@pytest.mark.slow` | Tests >5s — excluded from smoke runs |
