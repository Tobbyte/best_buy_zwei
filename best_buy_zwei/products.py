"""Product class for the Best Buy application."""

from typing import Any

from config import (
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

        Ensures it doesn't go below zero.
        Deactivates the product if quantity is zero.
        Be aware that setting a quantity above 0 when its not active
        - whether deliberately set or automatically because of 0
        quantity - will not automatically activate the product.
        Use activate() for that.
        """
        validated_qty = validate_non_negative_int("quantity", quantity)
        if validated_qty == 0:
            self.deactivate()

        self._quantity = validated_qty

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

        self.set_quantity(self._quantity - quantity)

        return float(quantity * self._price)


## debug
if __name__ == "__main__":
    print("=== Product debug/manual tests ===\n")

    # --- valid construction ---
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=3)
    assert mac.quantity == mac.get_quantity() == 100
    assert mac.active is True
    print("OK: construction + quantity/active accessors")

    # --- validation errors on construction ---
    bad_inputs = [
        ("", 10, 5, "empty name"),
        ("Valid", -5, 5, "negative price"),
        ("Valid", 10, -1, "negative quantity"),
        ("Valid", "10", 5, "non-numeric price"),
    ]
    for bad_name, bad_price, bad_qty, label in bad_inputs:
        try:
            Product(bad_name, price=bad_price, quantity=bad_qty)  # type: ignore
        except (TypeError, ValueError) as exc:
            print(f"OK: rejected {label} -> {exc}")
        else:
            print(f"FAILED: {label} was accepted but should have raised")

    # --- errors on external setting ---
    product = Product("Gadget", price=20, quantity=10)
    not_allowed = [
        ("name", "New Name"),
        ("price", 30),
        ("quantity", 5),
        ("active", False),
    ]
    for attr, new_value in not_allowed:
        try:
            setattr(product, attr, new_value)
        except AttributeError as exc:
            print(f"OK: rejected external change of {attr} -> {exc}")
        else:
            print(f"FAILED: external change of {attr} should raise")

    # --- quantity 0 on init leaves product inactive, activate() guards it ---
    empty = Product("Sold Out Gadget", price=20, quantity=0)
    assert empty.active is False
    print("OK: quantity 0 on init leaves product inactive")
    try:
        empty.activate()
    except ValueError as exc:
        print(f"OK: activate() on 0-quantity product rejected -> {exc}")
    else:
        print("FAILED: activate() should refuse a 0-quantity product")

    # --- buy(): happy path ---
    total = bose.buy(2)
    assert total == 500
    assert bose.quantity == 1
    print(
        f"OK: buy(2) -> {total} currency units, remaining stock {bose.quantity}",
    )

    # --- buy(): more than in stock ---
    try:
        bose.buy(5)
    except ValueError as exc:
        print(f"OK: buy() over stock rejected -> {exc}")
    else:
        print("FAILED: buying more than available stock should raise")

    # --- buy(): exactly the remaining stock deactivates the product ---
    bose.buy(1)
    assert bose.quantity == 0
    assert bose.active is False
    print("OK: buying the last unit deactivates the product automatically")

    # --- buy(): now-inactive product ---
    try:
        bose.buy(1)
    except ValueError as exc:
        print(f"OK: buy() on inactive product rejected -> {exc}")
    else:
        print("FAILED: buying an inactive product should raise")

    # --- buy(): zero quantity ---
    try:
        mac.buy(0)
    except ValueError as exc:
        print(f"OK: buy(0) rejected -> {exc}")
    else:
        print("FAILED: buy(0) should raise")
