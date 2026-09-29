# ruff:noqa
from best_buy_zwei.config import PRODUCT_PRETTY_PRINT
import pytest
from math import inf
from best_buy_zwei.products import NonStockedProduct

"""init
good
("unlimited", 100) => NonStockedProduct


bad
- überhaupt testen= weil s. Product?
"""


def test_NonStockedProduct_init_good():
    product = NonStockedProduct("Test Product", 10.99)
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.quantity == inf
    assert product.active is product.is_active() is True


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
"""


def test_NonStockedProduct_show(capsys):
    name, price, active = ("Gadget", 100, True)
    product = NonStockedProduct(name, price)
    product.show()
    captured = capsys.readouterr().out
    print(PRODUCT_PRETTY_PRINT(name, price, inf, active))
    expected = capsys.readouterr().out
    assert captured == expected


"""
buy
(2) =>
    self.quantity stays 0
    return (2 * self.price)

invalid 
s. super:
inactive        => ValueError w prod name
(0)             => ValueError w prod name
quant > stock   => ValueError w prod name
quant = -1      => ValueError w param name
"""


def test_NonStockedProduct_buy_valid():
    name, price = ("Gadget", 100)
    product = NonStockedProduct(name, price)
    result = product.buy(2)
    assert result == 2 * product.price
    assert product.quantity == inf


@pytest.mark.parametrize(
    "buy_quant, is_active",
    [(10, False), (0, True)],
)
def test_buy_invalid(buy_quant, is_active):
    product = NonStockedProduct("Gadget", 100)
    if not is_active:
        product.deactivate()

    with pytest.raises(ValueError) as err:
        product.buy(buy_quant)
    assert "Gadget" in str(err.value)


def test_buy_negative_quant():
    product = NonStockedProduct("Gadget", 100)
    with pytest.raises(ValueError) as err:
        product.buy(-1)
    assert "quantity" in str(err.value)


if __name__ == "__main__":
    pytest.main()
