# ruff: noqa
# type: ignore
from best_buy_zwei.products import Product
from best_buy_zwei.store import Store
import pytest


def test_store_contains_product():
    product = Product("Gadget", price=20, quantity=10)
    store = Store([product])
    another_product = Product("Another gadget", price=30, quantity=10)

    assert product in store
    assert another_product not in store


def test_store_add_combines_products_in_new_store():
    first_product = Product("First", price=10, quantity=1)
    second_product = Product("Second", price=20, quantity=1)
    first_store = Store([first_product])
    second_store = Store([second_product])

    combined_store = first_store + second_store

    assert combined_store is not first_store
    assert combined_store is not second_store
    assert combined_store.products == [first_product, second_product]


def test_store_add_does_not_share_product_list():
    first_product = Product("First", price=10, quantity=1)
    second_product = Product("Second", price=20, quantity=1)
    first_store = Store([first_product])
    second_store = Store([second_product])
    combined_store = first_store + second_store

    combined_store.add_product(Product("Extra", price=30, quantity=1))

    assert len(combined_store.products) == 3
    assert len(first_store.products) == 1
    assert len(second_store.products) == 1


if __name__ == "__main__":
    pytest.main(["test_store.py"])
