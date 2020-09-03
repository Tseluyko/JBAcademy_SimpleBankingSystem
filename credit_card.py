import random


class CreditCard:
    def __init__(self):
        self.mii = 400000
        self.id = random.randint(1, 999999999)
        self.checksum = random.randint(0, 9)
        self.pin = random.randint(1, 9999)
        self.balance = 0

    def get_card_number(self):
        number = str(self.mii)
        id_str = str(self.id)
        while len(id_str) < 9:
            id_str = '0' + id_str
        number += id_str
        number += str(self.checksum)
        return number

    def get_pin(self):
        str_pin = str(self.pin)
        while len(str_pin) < 4:
            str_pin = '0' + str_pin
        return str_pin

    def check_number(self, card_number):
        if len(card_number) != 16:
            return False
        mii = int(card_number[0:6])
        card_id = int(card_number[6:15])
        checksum = int(card_number[15])
        if mii != self.mii or card_id != self.id or checksum != self.checksum:
            return False
        return True

    def check_pin(self, pin):
        if int(pin) != self.pin:
            return False
        return True

    def get_balance(self):
        return self.balance
