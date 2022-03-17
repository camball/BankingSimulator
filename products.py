"""Defines a `Product` object, as well as wrapper functions for accessing a 
database of products."""
import sqlite3
from uuid import uuid4

PRODUCTS_DATABASE = "products.db"


def productExists(productUUID: str) -> bool:
    """Check if product with uuid `productUUID` exists in the products database."""
    con = sqlite3.connect(PRODUCTS_DATABASE)
    cur = con.cursor()
    cur.execute("SELECT uuid FROM products WHERE uuid = ?", (productUUID,))
    fetched_uuid = cur.fetchone()
    con.close()
    return True if fetched_uuid is not None else False


class ProductNotFoundError(sqlite3.ProgrammingError):
    """A more semantic error for when an entry is not found in the product database."""

    pass


class Product:
    """A product from the products database, retrieved and turned into an
    object that can be used in code.

    Has attributes `name` and `price`.
    """

    def __init__(self, productUUID: str) -> None:
        """Initialise a `Product` object.

        Make sure to check if the `productUUID` being passed in exists in the
        database first (by calling `products.productExists()`) before
        initialising a `Product` instance.
        """
        con = sqlite3.connect(PRODUCTS_DATABASE)
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE uuid = ?", (productUUID,))
        fetched_uuid, fetched_name, fetched_price = cur.fetchone()
        con.close()
        self.uuid = fetched_uuid
        self.name = fetched_name
        self.price = fetched_price  # represented in USD cents


def getProductByUUID(uuid: str) -> Product:
    """Returns a Product instance with data about a given product, given the
    hexadecimal UUID of said product.

    Raises a `products.ProductNotFoundError` if the product cannot be found."""
    if productExists(uuid):
        return Product(uuid)
    else:
        raise ProductNotFoundError


def initProductDatabase() -> None:
    """Create the database. Only intended to be run once."""
    response = input(
        f"""Are you sure you want to create a new table?\nThis may overwrite an existing {PRODUCTS_DATABASE} if it already exists. [y/n]: """
    )
    while True:
        if response[0].lower() == "y":
            con = sqlite3.connect(PRODUCTS_DATABASE)
            cur = con.cursor()
            cur.execute("CREATE TABLE products (uuid text, name text, price integer)")
            con.commit()
            con.close()
            break
        elif response[0].lower() == "n":
            break
        else:
            response = input("Please enter [y/n]: ")


def addProductToDatabase(name: str, price: int) -> None:
    """Add a product to the database. `price` must be supplied in USD cents."""
    con = sqlite3.connect(PRODUCTS_DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO products VALUES (?, ?, ?)", (uuid4().hex, name, price))
    con.commit()
    con.close()
