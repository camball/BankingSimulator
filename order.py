import random
import products
import sqlite3
from uuid import UUID, uuid4


def formatCentsToDollars(cents: int) -> str:
    """Takes in an arbitrary amount of cents; returns that amount of cents
    as a string formatted as \"$<dollars>.<cents>\"."""
    temp = str(cents)
    negative = bool()
    if cents < 0:
        temp = temp[1:]  # remove negative sign
        cents = abs(cents)
        negative = True

    if cents < 10:
        temp = "$0.0" + temp
    elif cents < 100:
        temp = "$0." + temp
    else:
        temp = "$" + temp[:-2] + "." + temp[-2:]
    return temp if not negative else f"-{temp}"


class BaseOrder:
    MAX_QUANTITY = 25
    """The maximum number of any individual product allowed in an order."""

    def __init__(self) -> None:
        """Initialise a `BaseOrder`.
        It should be noted that it is usually advised to
        instantiate an `Order` object instead of a `BaseOrder`.
        """
        self.productList: dict[str, int] = dict()
        self.orderID: UUID = uuid4()

    def __str__(self) -> str:
        output = f"Order {self.orderID.hex}\n"

        # print entry for each product in order
        for idx, (productName, quantity) in enumerate(self.productList.items()):
            try:
                p = products.getProductByName(productName)
                output += (
                    f"{idx + 1}. {quantity} of {productName} "
                    f"@ {formatCentsToDollars(p.price)} each\n"
                )
            except products.ProductNotFoundError:
                print(
                    """Something is very wrong with the order... 
                this needs fixing. A product should not have been added to the 
                order if it doesn't exist in the database..."""
                )

        output += f"TOTAL: {formatCentsToDollars(self.totalPrice)}"
        return output

    @property
    def totalPrice(self) -> int:
        """Total price of the order in USD cents."""
        prices = []
        for productName, quantity in self.productList.items():
            try:
                p = products.getProductByName(productName)
                prices.append(p.price * quantity)
            except products.ProductNotFoundError:
                print(
                    """Something is very wrong with the order... 
                this needs fixing. A product should not have been added to the 
                order if it doesn't exist in the database..."""
                )
        return sum(prices)

    def addProduct(self, productName: str) -> None:
        """Increment `product`'s quantity by one in the order, adding the
        product to the order if it is not already present.

        If `productName` is not a valid product (i.e., not added to the
        products database), then a `products.ProductNotFoundError is raised`.
        """
        if not products.productExists(productName):
            raise products.ProductNotFoundError

        if (quantity := self.productList.get(productName)) is None:
            self.productList[productName] = 1
        elif quantity <= self.MAX_QUANTITY:
            self.productList[productName] += 1

    def removeProduct(self, productName: str) -> None:
        """Decrement `product`'s quantity by one from the order, removing
        `product` entirely if the quantity is only one.

        If the product is not found, this method silently does nothing; it is
        the developer's responsibilty not to pass in a product that does not
        exist in the order (it doesn't make sense to intentionally have
        functionality for removing a product that was never added to the
        order - that would only occur when this method is called incorrectly).

        If `productName` is not a valid product (i.e., not added to the
        products database), then a `products.ProductNotFoundError is raised`.
        """
        if not products.productExists(productName):
            raise products.ProductNotFoundError

        if (val := self.productList.get(productName)) == 1:
            self.productList.pop(productName)  # key is guaranteed to exist here
        elif val is None:
            pass  # user of this function should never let program reach here
        else:
            self.productList[productName] -= 1

    def setQuantity(self, productName: str, quantity: int) -> None:
        """Instead of adding or removing a product, this function allows
        setting the quantity of a product directly.

        If a product is not in the order, it will be added to the order.
        If a product's quantity is set to zero, it will be removed from the
        order.

        If `productName` is not a valid product (i.e., not added to the
        products database), then a `products.ProductNotFoundError is raised`.
        """
        if not products.productExists(productName):
            raise products.ProductNotFoundError

        if quantity == 0:
            self.productList.pop(productName)
        elif productName not in self.productList.keys():
            self.productList[productName] = quantity
        elif quantity <= self.MAX_QUANTITY:
            if self.productList.get(productName):
                self.productList[productName] = quantity


class Order(BaseOrder):
    """Instances of `Order` contain a user-generated order.
    The `products` argument can be supplied, initialising the Order with a
    An `Order` contains a list of products.
    """

    def __init__(self, productDict: dict[str, int] | None = None) -> None:
        """Initialise an order. Passing a dictionary of products is optional,
        as products can be added to the order later as needed.

        If any product in `products` has a quantity of zero, it is silently not
        added to the order.

        If any product not in the products database is passed via `productDict`,
        it is silently not added to the order. All passed products should be
        validated (i.e., via `products.productExists()`).
        """
        super().__init__()
        if productDict:
            self.productList = {
                product: quantity
                for product, quantity in productDict.items()
                if quantity and products.productExists(product)
            }


class RandomOrder(BaseOrder):
    """An instance of `RandomOrder` contain a randomly generated order.
    This class is essentially only for system testing.
    """

    def __init__(self, numRandomProducts: int) -> None:
        """Initialise an order, with `numRandomProducts` randomly generated products."""
        super().__init__()

        con = sqlite3.connect("products.db")
        cur = con.cursor()
        products: list[tuple] = [
            name for name in cur.execute("SELECT name FROM products")
        ]
        con.close()

        random.seed()
        self.productList = {
            random.choice(products)[0]: random.randint(1, 5)
            for _ in range(numRandomProducts)
        }
