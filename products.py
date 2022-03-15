class BaseProduct:
    price: int  # represented in USD cents

    @property
    def name(self) -> str:
        return self.__class__.__name__


class Car(BaseProduct):
    price = 918236


class Truck(BaseProduct):
    price = 201980


class TractorTrailer(BaseProduct):
    price = 937297
