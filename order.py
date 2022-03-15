from math import prod
import random
import products
from uuid import UUID, uuid4


def centsToDollars(cents: int) -> str:
    return f"${int(cents / 100)}.{cents % 100}"


class BaseOrder:
    MAX_QUANTITY = 25
    """The maximum number of any individual product allowed in an order."""

    def __init__(self) -> None:
        """Initialise a `BaseOrder`.
        It should be noted that it is usually advised to
        instantiate an `Order` object instead of a `BaseOrder`.
        """
        self.productList: dict[products.BaseProduct, int] = dict()
        self.orderID: UUID = uuid4()

    def __str__(self) -> str:
        output = f"Order {self.orderID.hex}\n"
        for idx, (product, quanity) in enumerate(self.productList.items()):
            output += (
                f"{idx + 1}. {quanity} of {type(product).__name__} "
                f"@ {centsToDollars(product.price)} each\n"
            )
        output += f"TOTAL: {centsToDollars(self.totalPrice)}"
        return output

    @property
    def totalPrice(self) -> int:
        """Total price of the order in USD cents."""
        return sum(
            [product.price * quantity for product, quantity in self.productList.items()]
        )

    def addProduct(self, product: products.BaseProduct) -> None:
        """Increment `product`'s quantity by one in the order, adding the
        product to the order if it is not already present."""
        if (quantity := self.productList.get(product)) is None:
            self.productList[product] = 1
        elif quantity <= self.MAX_QUANTITY:
            self.productList[product] += 1

    def removeProduct(self, product: products.BaseProduct) -> None:
        """Decrement `product`'s quantity by one from the order, removing
        `product` entirely if the quantity is only one.

        If the product is not found, this method silently does nothing; it is
        the developer's responsibilty not to pass in a product that does not
        exist in the order (it doesn't make sense to intentionally have
        functionality for removing a product that was never added to the
        order - that would only occur when this method is called incorrectly).
        """
        if (val := self.productList.get(product)) == 1:
            self.productList.pop(product)  # key is guaranteed to exist here
        elif val is None:
            pass  # user of this function should never let program reach here
        else:
            self.productList[product] -= 1

    def setQuantity(self, product: products.BaseProduct, quantity: int) -> None:
        """Instead of adding or removing a product, this function allows
        setting the quantity of a product directly.
        """
        if 0 < quantity <= self.MAX_QUANTITY:
            if self.productList.get(product):
                self.productList[product] = quantity


class Order(BaseOrder):
    """Instances of `Order` contain a user-generated order.
    The `products` argument can be supplied, initialising the Order with a
    An `Order` contains a list of products.
    """

    def __init__(self, products: dict[products.BaseProduct, int] | None = None) -> None:
        """Initialise an order.
        Passing a dictionary of products is optional, as products can be added
        to the order later as needed.

        If any product in `products` has a quantity of zero, it is not added
        to the order.
        """
        super().__init__()
        if products:
            self.productList = {
                product: quantity for product, quantity in products.items() if quantity
            }


class RandomOrder(BaseOrder):
    """An instance of `RandomOrder` contain a randomly generated order.
    This class is essentially only for system testing.
    """

    def __init__(self, numRandomProducts: int) -> None:
        """Initialise an order, with `numRandomProducts` randomly generated products."""
        super().__init__()

        random.seed()
        self.productList = {
            random.choice(
                [products.Car, products.Truck, products.TractorTrailer]
            )(): random.randint(1, 5)
            for _ in range(numRandomProducts)
        }
