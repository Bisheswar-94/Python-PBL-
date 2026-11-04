# Online Shopping Cart

A simple storefront and shopping bag that demonstrates Python lists and tuples.

## Run

1. Install Python 3 (no third-party packages required).
2. Open a terminal in this folder.
3. Run `python web_app.py`.
4. Open http://127.0.0.1:8003.

The cart is stored locally in `cart_data.json`. Checkout is intentionally a demo message and does not process payments.

## Lists and tuples

- `PRODUCTS` in `shopping/store.py` is a list of product tuples. Each tuple stores `(id, name, category, price, stock)`. Tuples are immutable, making them suitable for fixed catalog entries.
- The cart is a list of tuples, each storing `(product_id, name, price, quantity)`.
- The program replaces a tuple in the list when quantity changes, because tuple contents cannot be edited in place.
- Functions add items, update quantities, calculate the total, and clear the cart.

## Structure

```text
Online Shopping Cart/
├── shopping/
│   ├── __init__.py
│   └── store.py
├── static/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── web_app.py
└── README.md
```
