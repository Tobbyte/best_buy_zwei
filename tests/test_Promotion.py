# ruff: noqa
# type: ignore
from best_buy_zwei.config import PRODUCT_PRETTY_PRINT
import pytest

from best_buy_zwei.products import (
    Product,
    Promotion,
    PromotedProduct,
    SecondHalfPrice,
    PercentDiscount,
    ThirdOneFree,
)


"""
PercentDiscount
init
valid
(product, PercentDiscount(30)) => price - 30%

0 discount => 0 reduction
invalid discount => TypeError
exceed max discount => ValueError


"""


def test_PercentDiscount_valid():
    product = Product("Gadget", 100, 10)
    disctounted = PercentDiscount(30)
    assert disctounted._discount == 30
    assert disctounted.apply_promotion(product.price, 2) == 140


def test_PercentDiscount_zero():
    product = Product("Gadget", 100, 10)
    disctounted = PercentDiscount(0)
    assert disctounted._discount == 0
    assert disctounted.apply_promotion(product.price, 2) == 200


def test_PercentDiscount_invalid_discount():
    discount = "30"
    with pytest.raises(TypeError):
        PercentDiscount(discount)


def test_PercentDiscount_exceed_max_discount():
    discount = 130
    with pytest.raises(ValueError):
        PercentDiscount(discount)


"""
SecondHalfPrice
init
valid
(product, SecondHalfPrice) => every 2. price*0.5
"""


@pytest.mark.parametrize(
    "buy_quant, reduced_price",
    [(0, 0), (1, 10), (2, 15), (3, 25), (4, 30), (8, 60), (11, 85)],
)
def test_SecondHalfPrice_valid(buy_quant, reduced_price):
    regular_price = 10
    product = Product("Gadget", regular_price, 100)
    disctounted = SecondHalfPrice()
    assert (
        disctounted.apply_promotion(product.price, buy_quant) == reduced_price
    )


"""
ThirdOneFree
init
valid
(product, ThirdOneFree) => every 3. free
"""


@pytest.mark.parametrize(
    "buy_quant, reduced_price",
    [(0, 0), (1, 10), (2, 20), (3, 20), (4, 30), (5, 40), (6, 40), (13, 90)],
)
def test_ThirdOneFree_valid(buy_quant, reduced_price):
    regular_price = 10
    product = Product("Gadget", regular_price, 100)
    disctounted = ThirdOneFree()
    assert (
        disctounted.apply_promotion(product.price, buy_quant) == reduced_price
    )


"""
PromotedProduct

(valid)
    => has products properties
    => displays description text in str

invalid prod => TypeError
buy => reduced price, reduced product stock
invalid buy => ValueError, product stock same
call w unknown properties => prop of product
# """


def test_PromotedProduct_valid():
    product = Product("Gadget", 100, 10)
    promoted = PromotedProduct(product, SecondHalfPrice())
    assert promoted.price == product.price
    assert "Second Half price!" in str(promoted)


def test_PromotedProduct_invalid_product():
    with pytest.raises(TypeError):
        PromotedProduct("product", SecondHalfPrice())


def test_PromotedProduct_buy_applies_promotion_reduces_stock():
    product = Product("Gadget", 100, 10)
    promoted = PromotedProduct(product, SecondHalfPrice())

    assert promoted.buy(2) == 150
    assert product.quantity == 8


def test_PromotedProduct_buy_too_many_no_stock_change():
    product = Product("Gadget", 100, 10)
    promoted = PromotedProduct(product, SecondHalfPrice())

    with pytest.raises(ValueError):
        promoted.buy(11)
    assert product.quantity == 10


def test_PromotedProduct_unknowns_passed_to_prod():
    product = Product("Gadget", 100, 10)
    promoted = PromotedProduct(product, SecondHalfPrice())

    assert promoted.price == 100
    assert promoted.name == "Gadget"


def test_multiple_promotions():
    product = Product("Gadget", 100, 10)
    promoted = PromotedProduct(
        product, [SecondHalfPrice(), PercentDiscount(20)]
    )

    assert promoted.buy(2) == 120
    assert product.quantity == 8


def test_multiple_promotions_order_independent():
    product = Product("Gadget", 100, 10)
    promoted1 = PromotedProduct(
        product, [SecondHalfPrice(), PercentDiscount(20)]
    )
    promoted2 = PromotedProduct(
        product, [PercentDiscount(20), SecondHalfPrice()]
    )

    assert promoted1.buy(2) == promoted2.buy(2)
    assert product.quantity == 6


if __name__ == "__main__":
    pytest.main(["test_Promotion.py"])
