# Best Buy CLI

A small command-line store application. Manage a product inventory and place orders through a menu-driven interface.

## Features

- Product inventory with three product types:
  - **Product** – regular, stocked item; deactivates automatically when its quantity reaches 0
  - **NonStockedProduct** – unlimited stock (e.g. licenses), quantity cannot be set
  - **LimitedProduct** – at most *n* purchases per order (e.g. shipping fee)
- **Promotions** applied via a `PromotedProduct` wrapper (see [Promotions](#promotions)):
  - `SecondHalfPrice` – every second item half price
  - `ThirdOneFree` – every third item free
  - `PercentDiscount` – percentage off
  - Multiple promotions can be stacked; they are applied in sequence
- Validated, type-casting CLI input via [`valid_tobbyte_module`](https://github.com/Tobbyte/valid_tobbyte_module)
- Unit tests for all product and promotion classes

## Promotions

Promotions are not baked into `Product`. Instead, `PromotedProduct` wraps any `Product` (or another `PromotedProduct`) together with one or more `Promotion` instances:

```python
from best_buy_zwei.products import Product, PromotedProduct, SecondHalfPrice, PercentDiscount

product = PromotedProduct(
    Product("USB-C Cable", price=10, quantity=250),
    SecondHalfPrice(),
)
total = product.buy(5)  # promotion applied on top of the regular buy()
```

The store stays ignorant of promotions: it accepts `PromotedProduct` wherever a `Product` is accepted, since the wrapper forwards attribute access to the wrapped product.

## Requirements

- Python 3.11+
- typing_extensions when Python < 3.12
- [`valid_tobbyte_module`](https://github.com/Tobbyte/valid_tobbyte_module) (used for validated CLI input)
- `pytest` for the test suite

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Menu options:
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit

While ordering, products are selected by number and added to a shopping cart. The cart contents are shown after every addition, and available quantities are adjusted for items already in the cart. Finishing the order places it and prints the total payment.

## Tests

```bash
python -m pytest best_buy_zwei
```

## Project structure

| File                  | Purpose                                                    |
|-----------------------|-------------------------------------------------------------|
| `main.py`             | Menu loop and ordering flow                                  |
| `products.py`         | `Product`, `NonStockedProduct`, `LimitedProduct`, promotions |
| `store.py`            | `Store` class (inventory, ordering)                          |
| `config.py`           | User-facing strings and prompts                              |
| `test_product.py`     | Tests for `Product`                                          |
| `test_NonStockProduct.py` | Tests for `NonStockedProduct`                            |
| `test_LimitedProduct.py`  | Tests for `LimitedProduct`                               |
| `test_Promotion.py`   | Tests for the promotion classes                              |

## Acknowledgement
- Made with ❤️ and without ai or code completion (except this readme)

## License

This project is licensed under the MIT License.
