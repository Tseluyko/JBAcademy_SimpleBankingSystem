import credit_card


class CustomerStorage:
    def __init__(self):
        self.storage = list()

    def add_new_customer(self):
        new_card = credit_card.CreditCard()
        self.storage.append(new_card)
        return [new_card.get_card_number(), new_card.get_pin()]

    def find_user(self, card_number):
        for card in self.storage:
            if card.check_number(card_number):
                return card

