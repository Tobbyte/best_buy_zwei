"""Main module for the Best Buy application.

Dear Reviewer, v2 notes:
I mainly added the PromotedProduct class and its associated promotion
classes.
The menu with its limitations are unchanged, since the focus of this
assignment was on working with classes. (Though I did add a little
feedback when adding to the shopping cart.)
Please see the note in PromotedProduct: I significantly changed the
implementation in contrast to the assignment description, but I think
you will agree with my design.


TODOs:
    - would be nice to show available products in cart when trying to
      place order exceeding quantity, but refrained from that for this
      submission bc of overhead.
    - use custom exceptions like ProductNotActiveError
    - TBD:
        - Should initializing of a Product with price 0 be possible?
          'None' if set with 0 seems more appropriate.
        - Shouldn't it be possible to buy an inactive product, think
          manual override by clerk as exception?
        - Store.get_total_quantity only gets quantity of active products
          which is inconsistent with fns name ("total" implies all).
          Ditto Store.get_all_products. But is requested, won't fix.
        - Should setting the quantity > 0 of an inactive product
          automatically activate it? Choose not to.
    - Ordering a cart processes the buying of the products in sequence.
      Order should be processed atomic.
    - _get_new_amount_selection has cheap fix against input 0. Needs
      proper solution in valid_tobbyte. Won't fix for now.
    - while ordering: unavailable products (all in card) shouldn't be
      selectable instead of failing with "0 available". bigger refactor,
      need to recalc menu etc. Won't fix for now.
    - make use of functools total_ordering
    - Buying a LimitedProduct shouldn't crash with an Exception, but
      its required by the assignment.
    - The design flaw that LimitedProducts and Promotions are not
      tracked per user is generously ignored for this assignment.


~ Made with ❤️ and without ai or code completion ~
"""

import sys
from pathlib import Path

from best_buy_zwei.bestbuy import BestBuyApp

# make runnable from wherever.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from best_buy_zwei.products import (
    LimitedProduct,
    NonStockedProduct,
    PercentDiscount,
    Product,
    PromotedProduct,
    SecondHalfPrice,
    ThirdOneFree,
)


def init_superstore() -> None:
    """Initialize the Best Buy application.

    Use a predefined set of products and start the menu interface.
    """
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
        PromotedProduct(
            Product("Extended Warranty", price=250, quantity=250),
            PercentDiscount(20),
        ),
        PromotedProduct(
            Product("USB-C Cable", price=10, quantity=250),
            SecondHalfPrice(),
        ),
        PromotedProduct(
            Product("USB-C Adapter", price=15, quantity=250),
            ThirdOneFree(),
        ),
        PromotedProduct(
            Product("Stacked Promo Exampl", price=50, quantity=250),
            [PercentDiscount(10), SecondHalfPrice(), ThirdOneFree()],
        ),
    ]
    BestBuyApp(product_list).start()


if __name__ == "__main__":
    init_superstore()
