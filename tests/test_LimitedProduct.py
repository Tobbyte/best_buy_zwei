# ruff: noqa
from best_buy_zwei.config import PRODUCT_PRETTY_PRINT
import pytest

from best_buy_zwei.products import LimitedProduct

"""
init
valid
("Fee", 10, 100, 1) => 
    NonStockedProduct
    maximum &  _maximum_initially == 1

invalid
("Fee", 10, 100, -1) => ValueError w. maximum
"""


def test_LimitedProduct_init_valid():
    name, price, quantity, maxi = ("Fee", 100, 10, 1)
    product = LimitedProduct(name, price, quantity, maxi)
    assert product.maximum == product._maximum_initially == maxi


def test_LimitedProduct_init_invalid():
    name, price, quantity, maxi = ("Fee", 100, 10, -1)
    with pytest.raises(ValueError) as err:
        LimitedProduct(name, price, quantity, maxi)
    assert "maximum" in str(err.value)


"""
set_maximum
(2)     => maximum ==  _maximum_initially == 2
(-1)    => ValueError w. prop name

"""


def test_LimitedProduct_set_maximum_valid():
    name, price, quantity, maxi = ("Fee", 100, 10, 1)
    product = LimitedProduct(name, price, quantity, maxi)
    product.set_maximum(2)
    assert product.maximum == product._maximum_initially == 2


"""
_set_maximum
("Fee", 10, 100, 1), _set_maximum(3)    => maximum == 3 != __maximum_initially == 1

"""


def test_LimitedProduct_set_maximum_internal():
    name, price, quantity, maxi = ("Fee", 10, 100, 1)
    product = LimitedProduct(name, price, quantity, maxi)
    product._set_maximum(3)
    assert product.maximum == 3
    assert product._maximum_initially == 1


"""
show()
() (active) => == PRODUCT_PRETTY_PRINT(..)
() (inactive) => == PRODUCT_PRETTY_PRINT(..)
"""


def test_LimitedProduct_show(capsys):
    name, price, quantity, maxi = ("Fee", 100, 10, 1)
    product = LimitedProduct(name, price, quantity, maxi)
    product.show()
    captured = capsys.readouterr().out
    print(PRODUCT_PRETTY_PRINT(name, price, quantity, True, maxi))
    expected = capsys.readouterr().out
    assert captured == expected


"""
buy
(2) =>
    self_maximum -= 2
    self_maximum_initially stays
    return (2 * self.price)

invalid
s. super:
inactive        => ValueError w prod name
(0)             => ValueError w prod name
quant > stock   => ValueError w prod name
quant = -1      => ValueError w param name

new:
quant > max (at once)   => ValueError w prod name, init.maximum
quant > max (consec)  => "
buy valid, set_maximum => resets _maximum_initially
"""


def test_LimitedProduct_buy_valid():
    name, price, quantity, maxi = ("Fee", 100, 10, 1)
    product = LimitedProduct(name, price, quantity, maxi)
    product.buy(1)
    assert product._maximum == maxi - 1
    assert product._maximum_initially == maxi


def test_LimitedProduct_buy_exceed_maximum_single():
    name, price, quantity, maximum = ("Gadget", 100, 10, 2)
    product = LimitedProduct(name, price, quantity, maximum)
    with pytest.raises(ValueError) as err:
        product.buy(10)
    assert all(str(var) in str(err.value) for var in [name, maximum])


def test_LimitedProduct_buy_exceed_maximum_consec():
    name, price, quantity, maximum = ("Gadget", 100, 10, 2)
    product = LimitedProduct(name, price, quantity, maximum)
    product.buy(1)
    product.buy(1)
    with pytest.raises(ValueError) as err:
        product.buy(1)
    assert all(str(var) in str(err.value) for var in [name, maximum])


def test_LimitedProduct_buy_valid_change_max_reset():
    name, price, quantity, maxi = ("Fee", 100, 10, 1)
    product = LimitedProduct(name, price, quantity, maxi)
    product.buy(1)
    product.set_maximum(3)
    assert product._maximum == 3
    assert product._maximum_initially == 3


if __name__ == "__main__":
    pytest.main()
