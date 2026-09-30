"""Configuration file for the Best Buy application."""
from math import inf

ORDER_PRODUCT_PROMPT = "Which product # do you want? (empty to exit) "
ORDER_EXIT_PROMPT = "When you want to finish order, enter empty text."
ORDER_AMOUNT_PROMPT = "What amount do you want? (empty to exit) "
ORDER_ADDED_TO_CART = "Product added to cart!"
ORDER_PLACED = "Order made! Total payment: ¤ {total:.2f}"
ORDER_ABORT = "Abort ordering."
ORDER_ERR_QUANT = (
    "Error placing item in cart: Only {quantity} items of '{name}' available."
)
ORDER_AVAILABLE_PRODUCTS = "Available products:"

MENU_TITLE = "Store Menu"
MENU_PROMPT = "Choose an item by its number [1 - {count}]: "
MENU_LIST_ALL_PRODUCTS = "List all products in store"
MENU_TOTAL_STORE_STOCK = "Show total amount in store"
MENU_PLACE_ORDER = "Make an order"
MENU_QUIT = "Quit"

ALL_PRODUCT_IN_STORE = "Products in store:"
NO_PRODUCTS_IN_STORE = "There are no products in the store."
TOTAL_STORE_STOCK_MSG = "Total of {total} (active) items in store."

PRODUCT_ERR_OUTOFSTOCK = "'{name}' is out of stock."
PRODUCT_ERR_CANTBYINACTIVE = "Can't buy inactive {name}."
PRODUCT_ERR_CANTBYZEROQUANT = "Can't buy 0 pcs of {name}."
PRODUCT_ERR_CANTACTIVATENULLQUANT = "Can't activate product with quantity 0."

NONSTOCKPRODUCT_ERR_CANTSETQUANTITY = (
    "Can't set quantity of NonStockedProduct."
)
LIMITED_PRODUCT_EXCEED_MAXIMUM = "Can't buy more than {maximum} pcs of {name}."


def PRODUCT_PRETTY_PRINT(  # noqa: ANN201, D103, N802
    name: str,
    price: float,
    quantity: float,  # pyright: ignore[reportRedeclaration]
    active: bool,
    maximum: int | None = None,
):
    if quantity == inf:
        quantity: str = "unlimited"
    return (
        f"'{name}', Price: {price:.2f} ¤, Quantity: {quantity}"
        + (" (inactive)" if not active else "")
        + (f" Limited to {maximum} per order!" if maximum else "")
    )

VALIDATE_ERR_NOT_OF_TYPE = "{name} is not of type {type}."
VALIDATE_ERR_STR_EMPTY = "{name} can't be empty."
VALIDATE_ERR_MUST_BE_POSITIVE = "{name} can't be negative."


ERR_NOT_PRODUCT = "Not of type <class 'Product'>"
ERR_NOT_PROMOTION = "Not of type <class 'Promotion'>"

SECONDHALFPRICE_DISPLAYTEXT = "Second Half price!"

THIRDONEFREE_DISPLAY_TEXT = "Third One Free!"
PROMOTION_PERCENTDISCOUNT_MAXDISCOUNT = 100
PROMOTION_PERCENTDISCOUNT_ERR_NOMORETHAN100 = "Can't discount more than 100%"
PERCENTDISCOUNT_DISPLAYTEXT = "{discount}% off!"
