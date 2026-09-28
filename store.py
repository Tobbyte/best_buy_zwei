"""Store class for the Best Buy application."""

from typing import Any

from config import (
    VALIDATE_ERR_NOT_OF_TYPE,
)
from products import Product


def _validate_is_product(name: str, value: Any) -> "Product":  # noqa: ANN401
    """Validate that value is a Product instance."""
    if not isinstance(value, Product):
        raise TypeError(
            VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="Product"),
        )
    return value


class Store:
    """A class representing a class in the Best Buy application.

    TODOs:
    - guard against inputting identical item. Won't fix.
    TBD:
    - It's questionable if order should be a method of Store.
    """

    _products: list[Product]


    def __init__(self, products: list[Product] | None = None) -> None:
        """Initialize a Store instance."""
        self._set_products(products)

    @property
    def products(self) -> list[Product]:
        """Return the list of products in the store.

        Use add_product() and remove_product() methods to modify
        the products in store.
        """
        return self._products

    def _set_products(self, products: list[Product] | None) -> None:
        """Set the list of products in the store."""
        if not products:
            self._products = []
            return

        if not isinstance(products, list):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="products",
                    type="list[Product]",
                ),
            )

        for prod in products:
            _validate_is_product("product", prod)

        self._products = products

    def add_product(self, product: Product) -> None:
        """Add a product to the store."""
        _validate_is_product("product", product)

        self._products.append(product)

    def remove_product(self, prod_to_rem: Product) -> None:
        """Remove a product from the store."""
        _validate_is_product("product", prod_to_rem)

        self._products = [
            prod_in_store
            for prod_in_store in self._products
            if prod_in_store is not prod_to_rem
        ]

    def get_total_quantity(self) -> int:
        """Return the total quantity of all active products in store."""
        return sum(
            prod.quantity for prod in self._products if prod.is_active()
        )

    def get_all_products(self) -> list[Product]:
        """Return a list of all active products in the store."""
        return [prod for prod in self._products if prod.is_active()]

    @staticmethod
    def order(shopping_list: list[tuple[Product, int]]) -> float:
        """Place an order of a list of products and their quantities.

        No validation here, since order shouldn't be a method of Store
        in the first place (at least how it's structured now).
        This is just to match the requirements.
        """
        return sum(item.buy(quant) for item, quant in shopping_list)


## debug
if __name__ == "__main__":
    print("=== Store debug/manual tests ===\n")

    mac = Product("MacBook Air M2", price=1450, quantity=5)
    bose = Product(
        "Bose QuietComfort Earbuds",
        price=250,
        quantity=0,
    )  # inactive
    pixel = Product("Google Pixel 7", price=500, quantity=10)

    store = Store([mac, bose, pixel])

    # --- get_all_products() / get_total_quantity() only count active items ---
    active_names = {p.name for p in store.get_all_products()}
    assert active_names == {"MacBook Air M2", "Google Pixel 7"}
    print(
        f"OK: get_all_products() excludes the inactive Bose -> {active_names}",
    )

    assert store.get_total_quantity() == 15
    print(
        f"OK: get_total_quantity() == {store.get_total_quantity()} (ignores inactive Bose)",
    )

    # --- add_product() / remove_product() ---
    extra = Product("iPad Mini", price=600, quantity=2)
    store.add_product(extra)
    assert "iPad Mini" in {p.name for p in store.get_all_products()}
    print("OK: add_product() adds a new product")

    store.remove_product(extra)
    assert "iPad Mini" not in {p.name for p in store.get_all_products()}
    print("OK: remove_product() removes it again")

    # --- add_product() type guard ---
    try:
        store.add_product("not a product")  # type: ignore
    except TypeError as exc:
        print(f"OK: add_product() rejects a non-Product value -> {exc}")
    else:
        print("FAILED: add_product() should reject non-Product values")

    # --- order(): happy path across multiple products ---
    total = Store.order([(mac, 1), (pixel, 2)])
    assert total == 1450 + 2 * 500
    print(f"OK: order() totals correctly -> {total}")
