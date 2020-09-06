from enum import Enum

from credit_card import CreditCard
import customer_storage


class State(Enum):
    MAIN_MENU = 0
    IN_ACCOUNT = 1
    ENTERING_NUMBER = 2
    ENTERING_PIN = 3
    INCOMING = 4
    TRANS_WELCOME = 5
    TRANS_MONEY = 6


class BankSystem:
    def __init__(self):
        self.storage = customer_storage.CustomerStorage()
        self.state = State.MAIN_MENU
        self.session_card_number = ''
        self.session_pin = ''
        self.transfer_dst = 0

    @staticmethod
    def get_main_menu():
        return '1. Create an account\n2. Log into account\n0. Exit\n'

    @staticmethod
    def get_user_menu():
        return '''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit\n'''

    @staticmethod
    def get_menu_number():
        return 'Enter your card number:\n'

    @staticmethod
    def get_menu_pin():
        return 'Enter your PIN:\n'

    @staticmethod
    def get_menu_income():
        return 'Enter income:\n'

    @staticmethod
    def get_menu_trans_welcome():
        return 'Enter card number:\n'

    @staticmethod
    def get_menu_trans_money():
        return 'Enter how much money you want to transfer:\n'

    def get_menu(self):
        if self.state == State.MAIN_MENU:
            return self.get_main_menu()
        if self.state == State.IN_ACCOUNT:
            return self.get_user_menu()
        if self.state == State.ENTERING_NUMBER:
            return self.get_menu_number()
        if self.state == State.ENTERING_PIN:
            return self.get_menu_pin()
        if self.state == State.INCOMING:
            return self.get_menu_income()
        if self.state == State.TRANS_WELCOME:
            return self.get_menu_trans_welcome()
        if self.state == State.TRANS_MONEY:
            return self.get_menu_trans_money()

    def emit_card(self):
        cn, pin = self.storage.add_new_customer()
        print('Your card has been created')
        print('Your card number:')
        print(cn)
        print('Your card PIN:')
        print(pin)

    def login_process(self):
        self.state = State.ENTERING_NUMBER

    def main_menu_processing(self, data):
        if data == '0':
            print("Bye!")
            exit(0)
        if data == '1':
            return self.emit_card()
        if data == '2':
            return self.login_process()

    def income_processing(self, data):
        self.storage.income_money(self.session_card_number, int(data))
        self.state = State.IN_ACCOUNT

    def user_menu_processing(self, data):
        if data == '0':
            print("Bye!")
            exit(0)
        if data == '1':
            balance = self.storage.get_balance(self.session_card_number)
            print(f'Balance: {balance}')
        if data == '2':
            self.state = State.INCOMING
        if data == '3':
            self.state = State.TRANS_WELCOME
        if data == '4':
            self.storage.delete_customer(self.session_card_number)
            print('The account has been closed!')
            self.session_card_number = None
            self.session_pin = None
            self.state = State.MAIN_MENU
        if data == '5':
            self.state = State.MAIN_MENU

    def entering_number_process(self, data):
        self.session_card_number = data
        self.state = State.ENTERING_PIN

    def entering_pin_process(self, data):
        self.session_pin = data
        return self.checking_process()

    def checking_process(self):
        card = self.storage.find_user(self.session_card_number)
        if not card:
            print('Wrong card number or PIN!')
            self.state = State.MAIN_MENU
            return
        if card[2] != self.session_pin:
            print('Wrong card number or PIN!')
            self.state = State.MAIN_MENU
            return
        print('You have successfully logged in!')
        self.state = State.IN_ACCOUNT

    def transfer_welcome(self, data):
        if self.session_card_number == data:
            print("You can't transfer money to the same account!")
            self.state = State.IN_ACCOUNT
            return
        if not CreditCard.ctrl_checksum(data):
            print("Probably you made a mistake in the card number. Please try again!")
            self.state = State.IN_ACCOUNT
            return
        if not self.storage.find_user(data):
            print("Such a card does not exist.")
            self.state = State.IN_ACCOUNT
            return
        self.transfer_dst = data
        self.state = State.TRANS_MONEY

    def transfer_money(self, data):
        if int(data) > self.storage.get_balance(self.session_card_number):
            print("Not enough money!")
            self.state = State.IN_ACCOUNT
            return
        self.storage.transfer_money(self.session_card_number,
                                    self.transfer_dst,
                                    int(data))
        print('Success!')
        self.state = State.IN_ACCOUNT

    def input_processing(self, data):
        if self.state == State.MAIN_MENU:
            return self.main_menu_processing(data)
        if self.state == State.IN_ACCOUNT:
            return self.user_menu_processing(data)
        if self.state == State.ENTERING_NUMBER:
            return self.entering_number_process(data)
        if self.state == State.ENTERING_PIN:
            return self.entering_pin_process(data)
        if self.state == State.INCOMING:
            return self.income_processing(data)
        if self.state == State.TRANS_WELCOME:
            return self.transfer_welcome(data)
        if self.state == State.TRANS_MONEY:
            return self.transfer_money(data)
