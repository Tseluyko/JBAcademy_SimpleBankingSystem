import random


class CreditCard:
    def __init__(self):
        self.mii = 400000
        self.id = random.randint(1, 999999999)
        self.checksum = 0
        self.checksum = self.generate_luhn_checksum()
        self.pin = random.randint(1, 9999)
        self.balance = 0

    def generate_luhn_checksum(self):
        numbers = self.get_card_number()[:15]
        l_sum = 0
        count = 0
        for num in numbers:
            if not count % 2:
                l_num = int(num) * 2
                if l_num > 9:
                    l_num -= 9
            else:
                l_num = int(num)
            l_sum += l_num
            count += 1
        checksum = 0
        while l_sum % 10:
            checksum += 1
            l_sum += 1
        return checksum

    def get_card_number(self):
        number = str(self.mii)
        id_str = str(self.id)
        while len(id_str) < 9:
            id_str = '0' + id_str
        number += id_str
        number += str(self.checksum)
        return number

    def get_id(self):
        return self.id

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
