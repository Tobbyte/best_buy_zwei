"""Product classes for the Best Buy application."""

from math import inf
from typing import Any

from best_buy_zwei.config import (
    LIMITED_PRODUCT_EXCEED_MAXIMUM,
    NONSTOCKPRODUCT_ERR_CANTSETQUANTITY,
    PRODUCT_ERR_CANTACTIVATENULLQUANT,
    PRODUCT_ERR_CANTBYINACTIVE,
    PRODUCT_ERR_CANTBYZEROQUANT,
    PRODUCT_ERR_OUTOFSTOCK,
    PRODUCT_PRETTY_PRINT,
    VALIDATE_ERR_MUST_BE_POSITIVE,
    VALIDATE_ERR_NOT_OF_TYPE,
    VALIDATE_ERR_STR_EMPTY,
)


def validate_non_empty_str(name: str, value: Any) -> str:  # noqa: ANN401
    """Validate that value is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="str"))
    if not value.strip():
        raise ValueError(VALIDATE_ERR_STR_EMPTY.format(name=name))
    return value


def validate_non_negative_num(name: str, value: Any) -> float | int:  # noqa: ANN401
    """Validate that value is a non-negative int or float."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="int or float"),
        )
    if value < 0:
        raise ValueError(VALIDATE_ERR_MUST_BE_POSITIVE.format(name=name))
    return value


def validate_non_negative_int(name: str, value: Any) -> int:  # noqa: ANN401
    """Validate that value is a non-negative integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="int"))
    if value < 0:
        raise ValueError(VALIDATE_ERR_MUST_BE_POSITIVE.format(name=name))
    return value


class Product:
    """A class representing a product in the Best Buy application.

    Attributes are protected and can be accessed via getters.
    Public setters are provided for quantity and active status.

    - TBD:
        - Raising ValueError when trying to buy more than available
          stock, trying to buy an inactive product or activating
          a product with 0 quantity is pretty harsh.

    """

    # Note to self: these are instance attribute annotations that define
    # the schema, and do not create a shared class state
    _name: str
    _price: float | int
    _quantity: int
    _active: bool

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Initialize a Product instance."""
        self._set_name(name)
        self._set_price(price)
        # important to use public set_quantity here to use validation
        self.set_quantity(quantity)
        self._active = quantity > 0

    @property
    def name(self) -> str:
        """Return the name of the product."""
        return self._name

    def _set_name(self, name: str) -> None:
        """Set the name of the product.

        Changing the name of a product is not planned for now, so
        no public setter is provided.
        """
        self._name = validate_non_empty_str("name", name)

    @property
    def price(self) -> float | int:
        """Return the price of the product."""
        return self._price

    def _set_price(self, price: float) -> None:
        """Set the price of the product.

        Changing the price of a product is not planned for now, so
        no public setter is provided.
        """
        self._price = validate_non_negative_num("price", price)

    @property
    def quantity(self) -> int:
        """Return the current quantity of the product.

        Use set_quantity() to modify the quantity, which includes
        validation and automatic deactivation.
        """
        return self._quantity

    def _set_quantity(self, quantity: int) -> None:
        """Set the quantity of the product.

        Internal setter for quantity to distinguish between calls from
        inside vs from outside.
        Ensures it doesn't go below zero.
        Deactivates the product if quantity is zero.
        """
        if quantity == 0:
            self.deactivate()
        self._quantity = quantity

    @property
    def active(self) -> bool:
        """Return whether the product is active.

        Use activate() and deactivate() methods to modify.
        """
        return self._active

    def get_quantity(self) -> int:
        """Return the current quantity of the product.

        Doubles property quantity, but is requirement.
        """
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        """Set the quantity of the product.

        Be aware that setting a quantity above 0 when its not active
        - whether deliberately set or automatically because of 0
        quantity - will not automatically activate the product.
        Use activate() for that.
        """
        validated_qty = validate_non_negative_int("quantity", quantity)
        if validated_qty == 0:
            self.deactivate()

        self._set_quantity(validated_qty)

    def is_active(self) -> bool:
        """Return whether product is available for purchase (active).

        Doubles property active, but is requirement.
        """
        return self._active

    def activate(self) -> None:
        """Activate the product, making it available for purchase.

        Raises ValueError if the product has zero quantity.
        """
        if self._quantity == 0:
            raise ValueError(PRODUCT_ERR_CANTACTIVATENULLQUANT)
        self._active = True

    def deactivate(self) -> None:
        """Deactivate the product, that is unavailable for purchase."""
        self._active = False

    def show(self) -> None:
        """Print product details in a user-friendly format."""
        print(
            PRODUCT_PRETTY_PRINT(
                self._name,
                self._price,
                self._quantity,
                self._active,
            ),
        )

    def buy(self, quantity: int) -> float:
        """Buy a specified quantity of the product.

        Raises ValueError if the product is inactive, if the quantity is
        negative, or if the requested quantity exceeds available stock.
        """
        if not self._active:
            raise ValueError(
                PRODUCT_ERR_CANTBYINACTIVE.format(name=self._name),
            )

        quantity = validate_non_negative_int("quantity", quantity)

        if quantity == 0:
            raise ValueError(
                PRODUCT_ERR_CANTBYZEROQUANT.format(
                    name=self._name,
                ),
            )

        if quantity > self._quantity:
            raise ValueError(PRODUCT_ERR_OUTOFSTOCK.format(name=self._name))

        self._set_quantity(self._quantity - quantity)

        return float(quantity * self._price)


class NonStockedProduct(Product):
    """A class representing a product with unlimited quantity.

    Note: The assignment states "the quantity should be set to zero and
    always stay that way". I have decided to consciously deviate:
    A quantity of 0 already has a distinct meaning and operations
    depending on a 0 quantity. NonStockProduct having a quantity 0
    would mean to work around that introducing fragility.
    Also, infinite simply makes more sense and enables minimum overhead.
    """

    _quantity: float

    def __init__(self, name: str, price: float) -> None:
        """Initialize a Product instance."""
        self._set_name(name)
        self._set_price(price)
        self._active = True
        self._quantity = inf

    def set_quantity(self) -> None:
        """Override super class.

        Since there's always unlimited quantity, it can't be
        set like in a regular Product.
        Raises NotImplementedError if called.

        """
        raise NotImplementedError(NONSTOCKPRODUCT_ERR_CANTSETQUANTITY)


class LimitedProduct(Product):
    """A class representing a Product that can be bought n times.

    TBD:
    - The existence of such a Product class is questionable: A shipping
    fee as e.g. should be added automatically and therefore could be a
    normal but non-user facing product. If it should be used like a
    "limited offer" per user or similar, there has to be a user tracking
    which, again, would be fine with a regular Product of limited
    quantity since tracking has to be done in the Store ...
    Better would be a flag in the Store class marking which products
    are of limited availability and add some special items like fees
    automatically.
    . Won't fix as it's requested.
    - I a remaining maximum of zero should deactivate the product is not
    defined. Chose not to.
    """

    _maximum: int  # bad name, but given.
    _maximum_initially: int  # for output purposes

    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        maximum: int,
    ) -> None:
        """Initialize a Product instance."""
        super().__init__(name, price, quantity)
        # important to use public set_maximum here to use validation
        self.set_maximum(maximum)
        self._maximum_initially = maximum

    @property
    def maximum(self) -> int:
        """Return the maximum buyability of the product."""
        return self._maximum

    def _set_maximum(self, maximum: int) -> None:
        """Set the internal _maximum of the product.

        Internal setter for maximum that doesn't resets
        _maximum_initially.
        """
        self._maximum = maximum

    def set_maximum(self, maximum: int) -> None:
        """Set the maximum buyability of the product."""
        valid_max = validate_non_negative_int("maximum", maximum)
        self._set_maximum(valid_max)
        self._maximum_initially = maximum

    def show(self) -> None:
        """Print product details in a user-friendly format."""
        print(
            PRODUCT_PRETTY_PRINT(
                self._name,
                self._price,
                self._quantity,
                self._active,
                self._maximum_initially,
            ),
        )

    def buy(self, quantity: int) -> float:
        """Buy a specified quantity of the product.

        Raises ValueError if the requested quantity exceeds
        the maximum limit.
        """
        if quantity > self._maximum:
            raise ValueError(
                LIMITED_PRODUCT_EXCEED_MAXIMUM.format(
                    maximum=self._maximum_initially,
                    name=self._name,
                ),
            )

        self._set_maximum(self._maximum - quantity)

        return super().buy(quantity)
