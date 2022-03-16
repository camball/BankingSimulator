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
    MyOrder = order.Order()
    print(MyOrder, "\n")

    MyOrder.addProduct("Truck")
    MyOrder.addProduct("Car")
    print(MyOrder, "\n")

    MyOrder.setQuantity("Tractor Trailer", 4)
    MyOrder.removeProduct("Car")
    print(MyOrder, "\n")

    # TODO: Fix order class to hash dictionary with *constant* product lookup codes instead of instances of the products. Adds and removes don't work right in that case.


if __name__ == "__main__":
    main()
