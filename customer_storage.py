import credit_card
import sqlite3


class CustomerStorage:
    def __init__(self):
        self.db_connect = sqlite3.connect('card.s3db')
        self.db_cursor = self.db_connect.cursor()
        self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card'")
        result = self.db_cursor.fetchone()
        if not result:
            self.db_cursor.execute('''CREATE TABLE card(
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0);''')
            self.db_connect.commit()

    def add_new_customer(self):
        new_card = credit_card.CreditCard()
        self.db_cursor.execute(f'''INSERT INTO card
        VALUES({new_card.get_id()},
        {new_card.get_card_number()},
        {new_card.get_pin()},
        {new_card.get_balance()});''')
        self.db_connect.commit()
        return [new_card.get_card_number(), new_card.get_pin()]

    def find_user(self, card_number):
        self.db_cursor.execute(f'''SELECT * FROM card WHERE number = {card_number};''')
        return self.db_cursor.fetchone()


