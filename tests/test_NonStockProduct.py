# ruff:noqa
from best_buy_zwei.config import PRODUCT_PRETTY_PRINT
import pytest
from math import inf
from best_buy_zwei.products import NonStockedProduct

"""init
good
("unlimited", 100) => NonStockedProduct

bad
test same validators as in Product excl. for quantity
"""


def test_NonStockedProduct_init_good():
    product = NonStockedProduct("Test Product", 10.99)
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.quantity == inf
    assert product.active is product.is_active() is True


@pytest.mark.parametrize(
    "name, price, result",
    [
        (123, 100, TypeError),  # invalid name
        (" ", 100, ValueError),  # invalid name
        ("good_name", "100", TypeError),  # invalid price
    ],
)
def test_product_init_bad(name, price, result):
    with pytest.raises(result):
        NonStockedProduct(name, price)


"""
set_quantity
() => Notimplemented Error
"""


def test_NonStockedProduct_set_quantity_forbidden():
    product = NonStockedProduct("Gadget", price=20)
    with pytest.raises(NotImplementedError):
        product.set_quantity()


"""
show
() => "unlimited" in stdout
but no need to test since its implemented in PRODUCT_PRETTY_PRINT
and not changed in NonStockedProduct
"""

pass


"""
buy
(200000000000) =>
    self.quantity stays inf
    return (200000000000 * self.price)

no new fail cases to super, don't test?
"""


def test_NonStockedProduct_buy_valid():
    name, price = ("Gadget", 100)
    product = NonStockedProduct(name, price)
    result = product.buy(200000000000)
    assert result == 200000000000 * product.price
    assert product.quantity == inf


if __name__ == "__main__":
    pytest.main()
