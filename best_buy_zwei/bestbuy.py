"""Best Buy application."""

import sys

from best_buy_zwei.config import (
    ALL_PRODUCT_IN_STORE,
    MENU_LIST_ALL_PRODUCTS,
    MENU_PLACE_ORDER,
    MENU_PROMPT,
    MENU_QUIT,
    MENU_TITLE,
    MENU_TOTAL_STORE_STOCK,
    NO_PRODUCTS_IN_STORE,
    ORDER_ABORT,
    ORDER_ADDED_TO_CART,
    ORDER_AMOUNT_PROMPT,
    ORDER_AVAILABLE_PRODUCTS,
    ORDER_ERR_QUANT,
    ORDER_EXIT_PROMPT,
    ORDER_PLACED,
    ORDER_PRODUCT_PROMPT,
    TOTAL_STORE_STOCK_MSG,
)
from best_buy_zwei.products import Product
from best_buy_zwei.store import Store
from best_buy_zwei.valid_tobbyte_module.valid_tobbyte.validator_fn import (
    validate_fn as get_valid_input,
)


class BestBuyApp:  # pylint: disable=R0903
    """The Best Buy application."""

    def __init__(self, product_list: list | None = None) -> None:
        """Init a new instance."""
        self.store = Store(product_list)

    def _place_order(self) -> None:  # noqa: C901
        """Place an order for products.

        Prompts user to select products and quantities, adds them to a
        shopping cart, and processes the order.
        """
        print(ORDER_AVAILABLE_PRODUCTS)
        shopping_cart = []
        product_selection = None
        amount_selection = None
        available_products = self.store.get_all_products()

        def _get_amount_in_cart(product: Product) -> int:
            return sum([tup[1] for tup in shopping_cart if tup[0] is product])

        def _should_abort() -> bool:
            # Print abort msg if card is empty.
            # Used in check on empty input
            if not shopping_cart:
                print("\n" + ORDER_ABORT)
                return True
            return False

        def _get_new_product_selection() -> int | None:
            return get_valid_input(
                valid_inputs=[
                    *list(range(1, len(available_products) + 1)),
                ],
                prompt=ORDER_PRODUCT_PROMPT,
                exit_prompt="",
            )

        def _get_new_amount_selection() -> int | None:
            while True:
                # cheap fix. need to be handled cleanly
                # by valid_tobbyte_module. ok for now.
                # Entering 0 will be treated as empty and exit the menu.
                # Not very nice but accepted for now.
                inp = get_valid_input(
                    valid_inputs=[int],
                    prompt=ORDER_AMOUNT_PROMPT,
                    exit_prompt="",
                )
                if not inp or inp > 0:
                    break
            return inp

        def _print_cart() -> None:
            if not shopping_cart:
                print("(cart is empty)")
                return
            print("In cart:")
            for prod, qty in shopping_cart:
                print(f"  {qty}x {prod.name}")

        def _confirm_order() -> None:
            print("\n\n***********")
            print(ORDER_PLACED.format(total=self.store.order(shopping_cart)))
            print("***********")

        # construct and print product selection menu
        for i, avail_prod in enumerate(available_products):
            print(f"{i + 1}: ", end="")
            print(avail_prod)

        print("\n" + ORDER_EXIT_PROMPT + "\n")

        # loop ordering
        while True:
            new_product_selection = _get_new_product_selection()

            if not new_product_selection:
                # returned from product selection menu wo selection
                if _should_abort():
                    # made not prev. placement, abort to main menu
                    return
                break

            product_selection = new_product_selection - 1  # reset from display

            new_amount_selection = _get_new_amount_selection()

            if not new_amount_selection:
                # returned from amount selection menu wo selection
                if _should_abort():
                    # made not prev. placement, abort to main menu
                    return
                break

            items_of_product_available = available_products[
                product_selection
            ].get_quantity() - _get_amount_in_cart(
                available_products[product_selection],
            )

            if new_amount_selection > items_of_product_available:
                # user selected more than available
                print(
                    ORDER_ERR_QUANT.format(
                        quantity=items_of_product_available,
                        name=available_products[product_selection].name,
                    ),
                )

            else:
                # user selected valid amount, add to shopping card
                amount_selection = new_amount_selection

                shopping_cart.append((
                    available_products[product_selection],
                    amount_selection,
                ))

                print()
                print(ORDER_ADDED_TO_CART)
                _print_cart()
                print()

        if shopping_cart:
            _confirm_order()
        return

    def _print_all_products(self) -> None:
        """Print all products in the store."""
        print(ALL_PRODUCT_IN_STORE)
        all_products = self.store.get_all_products()
        if not all_products:
            print(NO_PRODUCTS_IN_STORE)
        else:
            for prod in all_products:
                print(prod)

    def _get_total_store_stock(self) -> None:
        """Print the total quantity of all products in the store."""
        print(
            TOTAL_STORE_STOCK_MSG.format(
                total=self.store.get_total_quantity(),
            ),
        )

    def start(self) -> None:
        """Start the Best Buy application."""
        print()
        print(MENU_TITLE)
        menu_dispatch = {
            1: (MENU_LIST_ALL_PRODUCTS, self._print_all_products),
            2: (MENU_TOTAL_STORE_STOCK, self._get_total_store_stock),
            3: (MENU_PLACE_ORDER, self._place_order),
            4: (MENU_QUIT, sys.exit),
        }
        while True:
            print("------")

            # print menu options
            for k, (label, _) in menu_dispatch.items():
                print(f"{k}: {label}")

            print()
            selection = get_valid_input(
                valid_inputs=list(range(1, len(menu_dispatch) + 1)),
                prompt=MENU_PROMPT.format(count=len(menu_dispatch)),
            )

            if not selection:  # exit by double enter none in get_valid_input
                sys.exit()

            print()
            print("------")
            menu_dispatch[selection][1]()
            print()
