# ruff:noqa
from best_buy_zwei.config import PRODUCT_PRETTY_PRINT
import pytest
from best_buy_zwei.products import (
    Product,
    validate_non_negative_int,
    validate_non_negative_num,
    validate_non_empty_str,
)


"""
validate_non_negative_int
3 => 3
0 => 0
-1 => VE VALIDATE_ERR_MUST_BE_POSITIVE für "name"
True => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
2.0 => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
"2.0" => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
None => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
"""


@pytest.mark.parametrize("value, result", [(3, 3), (0, 0)])
def test_validate_non_negative_int_for_valid_calls(value, result):
    assert validate_non_negative_int("_", value) == result


def test_validate_non_negative_int_ValueE_for_negative():
    with pytest.raises(ValueError) as err:
        validate_non_negative_int("bezeichner", -1)
    assert "bezeichner" in str(err.value)


@pytest.mark.parametrize("value", [True, 2.0, "2.0", None])
def test_validate_non_negative_int_TypeE_for_bad_type(value):
    with pytest.raises(TypeError) as err:
        validate_non_negative_int("bezeichner", value)
    assert "bezeichner" in str(err.value)


"""
validate_non_negative_num
3       => 3
3.0     => 3.0
0       => 0

-1      => ValueError w name

True    => TypeError w name
"2.0"   => "
None    => "
"""


@pytest.mark.parametrize("value, result", [(3, 3), (3.0, 3.0), (0, 0)])
def test_validate_non_negative_num_valid_calls(value, result):
    assert validate_non_negative_num("_", value) == result


def test_validate_non_negative_num_ValueE_for_negative():
    with pytest.raises(ValueError) as err:
        validate_non_negative_num("bezeichner", -1)
    assert "bezeichner" in str(err.value)


@pytest.mark.parametrize("value", (True, "2.0", None))
def test_validate_non_negative_num_TypeE_for_bad_type(value):
    with pytest.raises(TypeError) as err:
        validate_non_negative_num("bezeichner", value)
    assert "bezeichner" in str(err.value)


"""
validate_non_empty_str
"bla"       => "bla"
2           => TypeError w name
True        => "
None        => "
""          => ValueError w name
" "         => "
"""


def test_validate_non_empty_str_valid_call():
    assert validate_non_empty_str("_", "bla") == "bla"


@pytest.mark.parametrize("value", [2, True, None])
def test_validate_non_empty_str_TypeError_for_bad_type(value):
    with pytest.raises(TypeError) as err:
        validate_non_empty_str("bezeichner", value)
    assert "bezeichner" in str(err.value)


@pytest.mark.parametrize("value", ["", " "])
def test_validate_non_empty_str_ValueError_for_bad_type(value):
    with pytest.raises(ValueError) as err:
        validate_non_empty_str("bezeichner", value)
    assert "bezeichner" in str(err.value)


"""
__init
good init    => Product
bad inputs in init:
test if /any/ error is thrown, we need to test the
wiring of the validators, which are tested on their own above.
bad name, price, quantity => Value/TypeError
"""


def test_product_init_good():
    product = Product("Test Product", 10.99, 5)
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.quantity == product.get_quantity() == 5
    assert product.active is product.is_active() is True


@pytest.mark.parametrize(
    "name, price, quant, result",
    [
        (123, 100, 10, TypeError),  # invalid name
        (" ", 100, 10, ValueError),  # invalid name
        ("good_name", "100", 10, TypeError),  # invalid price
        ("good_name", 100, "10", TypeError),  # invalid quant
    ],
)
def test_product_init_bad(name, price, quant, result):
    with pytest.raises(result):
        Product(name, price, quant)


"""
setting directly
quant, name, price, active => AttributeError
"""


@pytest.mark.parametrize(
    "attr, new_val",
    [("name", "watevr"), ("price", 3), ("quantity", 5), ("active", False)],
)
def test_product_disallow_external_setattr(attr, new_val):
    product = Product("Gadget", price=20, quantity=10)

    with pytest.raises(AttributeError) as err:
        setattr(product, attr, new_val)
    assert attr in str(err.value)


"""
set_quantity()
3 => 3
0 => 0,  active == False
-1 => is exception, s. init
is not active (auto), set quant 10 => not active
is not active (mani), set quant 10 => not active
"""


def test_product_set_quantity_valid():
    product = Product("Gadget", price=20, quantity=10)
    product.set_quantity(3)
    assert product.quantity == 3


def test_product_set_quantity_0_with_deactivation():
    product = Product("Gadget", price=20, quantity=10)
    product.set_quantity(0)
    assert product.quantity == 0 and product.active == False


def test_product_set_quantity_invalid():
    product = Product("Gadget", price=20, quantity=10)
    with pytest.raises(ValueError):
        product.set_quantity(-1)


def test_product_set_quantity_when_inactive_auto():
    product = Product("Gadget", price=20, quantity=0)
    product.set_quantity(10)
    assert not product.active


def test_product_set_quantity_when_inactive_manu():
    product = Product("Gadget", price=20, quantity=10)
    product.deactivate()
    product.set_quantity(20)
    assert not product.active


"""
deactivate()
() => prod.active == False
"""


def test_product_deactivate():
    product = Product("Gadget", price=20, quantity=10)
    product.deactivate()
    assert product.active == product.is_active() == False


"""activate()
() => product.active == True
() if prod.quantity == 0 => ValueError
"""


def test_product_activate():
    product = Product("Gadget", price=20, quantity=10)
    product.deactivate()
    product.activate()
    assert product.active == product.is_active() == True


def test_product_activate_when_inactive():
    product = Product("Gadget", price=20, quantity=0)
    with pytest.raises(ValueError):
        product.activate()


"""
show()
() (active) => == PRODUCT_PRETTY_PRINT(..)
() (inactive) => == PRODUCT_PRETTY_PRINT(..)
"""


def test_product_show(capsys):
    name, price, quantity, active = ("Gadget", 100, 10, True)
    product = Product(name, price, quantity)
    product.show()
    captured = capsys.readouterr().out
    print(PRODUCT_PRETTY_PRINT(name, price, quantity, active))
    expected = capsys.readouterr().out
    assert captured == expected


def test_product_show_for_inactive(capsys):
    name, price, quantity, active = ("Gadget", 100, 0, False)
    product = Product(name, price, quantity)
    product.show()
    captured = capsys.readouterr().out
    print(PRODUCT_PRETTY_PRINT(name, price, quantity, active))
    expected = capsys.readouterr().out
    assert captured == expected


"""
buy()

(2) =>
    set self.quantity -2,
    return float(2*self.price)
(10) (stock 10) => product.active == False
inactive        => ValueError w prod name
(0)             => ValueError w prod name
quant > stock   => ValueError w prod name
quant = -1      => ValueError w param name
"""


def test_buy_valid():
    name, price, quantity = ("Gadget", 100, 10)
    product = Product(name, price, quantity)
    result = product.buy(2)
    assert result == 2 * product.price
    assert product.quantity == quantity - 2


def test_buy_valid_all_stock_deactivates():
    name, price, quantity = ("Gadget", 100, 10)
    product = Product(name, price, quantity)
    result = product.buy(10)
    assert result == 10 * product.price
    assert product.quantity == quantity - 10
    assert not product.active


@pytest.mark.parametrize(
    "buy_quant, stock, is_active",
    [(10, 100, False), (101, 100, True), (0, 100, True)],
)
def test_buy_invalid(buy_quant, stock, is_active):
    product = Product("Gadget", 100, stock)
    if not is_active:
        product.deactivate()

    with pytest.raises(ValueError) as err:
        product.buy(buy_quant)
    assert "Gadget" in str(err.value)


def test_buy_negative_quant():
    product = Product("Gadget", 100, 10)
    with pytest.raises(ValueError) as err:
        product.buy(-1)
    assert "quantity" in str(err.value)


if __name__ == "__main__":
    pytest.main()
