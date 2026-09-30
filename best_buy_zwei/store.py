"""Store class for the Best Buy application."""

from typing import Any

from best_buy_zwei.config import (
    VALIDATE_ERR_NOT_OF_TYPE,
)
from best_buy_zwei.products import Product, PromotedProduct


def _validate_is_product(name: str, value: Any) -> "Product | PromotedProduct":  # noqa: ANN401
    """Validate that value is a Product instance."""
    if not isinstance(value, Product | PromotedProduct):
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

    def __contains__(self, product: object) -> bool:
        """Return whether a product is present in the store."""
        return product in self._products

    def __add__(self, other: object) -> "Store":
        """Return a new store containing products from both stores."""
        if not isinstance(other, Store):
            return NotImplemented
        return Store(self._products + other.products)

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
