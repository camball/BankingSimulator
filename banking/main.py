import products
import order


def main():
    """
    As far as functionality goes, the following is what I want to happen:
    1. Have a bunch of random products in an order.
    2. From the company's perspective, they just get a bunch of orders in. We can represent this as a queue.
    3. Build a BankAccount class.
    4. Process the queue of orders - i.e., take the money out of the customer's bank account and add it to the company's account.
    """

    """
    Developer Flow for using UUIDs instead of human-readable strings for DB primary key:
    1. Search for product in database by name (if they don't already have the UUID from another source)
    2. If a result is found, return it's UUID
    3. Developer can save that UUID to a variable to make it easy, like:
        carID = searchDatabaseByName("Car")
    4. Pass that UUID to the order methods, like:
        order.addProduct(carID)
    """

    MyOrder = order.Order()
    print(MyOrder, "\n")

    MyOrder.addProduct("8754582704f74ed3ad23e53692f799b5")  # Truck
    MyOrder.addProduct("bd199e7626064238a1c1a0554d970323")  # Car
    print(MyOrder, "\n")

    MyOrder.setQuantity("e76e6eeade6c492286b6461d33d7477b", 4)  # Tractor Trailer
    MyOrder.removeProduct("bd199e7626064238a1c1a0554d970323")  # Car
    print(MyOrder, "\n")


if __name__ == "__main__":
    main()
