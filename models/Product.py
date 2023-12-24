class Product:
    def __init__(self, id, name, price, discount):
        self.id = id
        self.name = name
        self.price = price
        self.discount = discount  # in percent 0.5 => 50%

    def __str__(self):
        return f"ID = {self.id}\nNAME = {self.name}\nPRICE = {self.price}\nDISCOUNT = {self.discount}"

    def get_price(self):
        if self.discount is not None and self.discount != 0:
            return self.discounted_price()
        return self.price

    def discounted_price(self):
        if self.discount is not None and self.discount != 0:
            return self.price * self.discount
        return self.price
