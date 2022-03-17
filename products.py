"""Defines a `Product` object, as well as wrapper functions for accessing a 
database of products."""
import sqlite3
from uuid import uuid4


def productExists(productName: str) -> bool:
    """Check if product with name `productName` exists in the products database."""
    con = sqlite3.connect("products.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM products WHERE name = ?", (productName,))
    fetched_name = cur.fetchone()
    con.close()
    return True if fetched_name is not None else False


class ProductNotFoundError(sqlite3.ProgrammingError):
    """A more semantic error for when an entry is not found in the product database."""

    pass


class Product:
    """A product from the products database, retrieved and turned into an
    object that can be used in code.

    Has attributes `name` and `price`.
    """

    def __init__(self, productName: str) -> None:
        """Initialise a `Product` object.

        Make sure to check if the `productName` being passed in exists in the
        database first (by calling `products.productExists()`) before
        initialising a `Product` instance.
        """
        con = sqlite3.connect("products.db")
        cur = con.cursor()
        cur.execute("SELECT name, price FROM products WHERE name = ?", (productName,))
        fetched_name, fetched_price = cur.fetchone()
        con.close()
        self.name = fetched_name
        self.price = fetched_price  # represented in USD cents


def getProductByName(name: str) -> Product:
    """Returns a Product instance with data about a given product, given the
    name of said product.

    Raises a `products.ProductNotFoundError` if the product cannot be found."""
    if productExists(name):
        return Product(name)
    else:
        raise ProductNotFoundError


def initProductDatabase() -> None:
    """Create the database. Only intended to be run once."""
    response = input(
        """Are you sure you want to create a new table? This may 
    overwrite an existing products.db if it already exists. [y/n]: """
    )
    while True:
        if response[0].lower() == "y":
            con = sqlite3.connect("products.db")
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
    con = sqlite3.connect("products.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO products VALUES ('{uuid4()}','{name}','{price}')")
    con.commit()
    con.close()
