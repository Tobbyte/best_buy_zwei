import pytest
from best_buy_zwei.products import Product


def test_product_initialization():
    product = Product("Test Product", 10.99, 5)
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.quantity == 5
    assert product.active is True
