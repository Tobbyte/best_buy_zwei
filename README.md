# Best Buy CLI

A small command-line store application. Manage a product inventory and place orders through a menu-driven interface.

## Requirements

- Python 3.10+
- [`valid_tobbyte_module`](https://github.com/Tobbyte/valid_tobbyte_module) (used for validated CLI input)

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

## Project structure

| File                  | Purpose                                       |
|------------------------|------------------------------------------------|
| `main.py`              | Menu loop and ordering flow                    |
| `products.py`          | `Product` class                                |
| `store.py`             | `Store` class (inventory, ordering)            |
| `config.py`            | User-facing strings and prompts                |


## Acknowledgement
- Made with ❤️ and without ai or code completion (except this readme)