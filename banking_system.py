from enum import Enum

import credit_card
import customer_storage


class State(Enum):
    MAIN_MENU = 0
    IN_ACCOUNT = 1
    ENTERING_NUMBER = 2
    ENTERING_PIN = 3


class BankSystem:
    def __init__(self):
        self.storage = customer_storage.CustomerStorage()
        self.state = State.MAIN_MENU
        self.session_card_number = ''
        self.session_pin = ''
        self.session_card = None

    @staticmethod
    def get_main_menu():
        return '1. Create an account\n2. Log into account\n0. Exit\n'

    @staticmethod
    def get_user_menu():
        return '1. Balance\n2. Log out\n0. Exit\n'

    @staticmethod
    def get_menu_number():
        return 'Enter your card number:\n'

    @staticmethod
    def get_menu_pin():
        return 'Enter your PIN:\n'

    def get_menu(self):
        if self.state == State.MAIN_MENU:
            return self.get_main_menu()
        if self.state == State.IN_ACCOUNT:
            return self.get_user_menu()
        if self.state == State.ENTERING_NUMBER:
            return self.get_menu_number()
        if self.state == State.ENTERING_PIN:
            return self.get_menu_pin()

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
            exit(0)
        if data == '1':
            return self.emit_card()
        if data == '2':
            return self.login_process()

    def user_menu_processing(self, data):
        if data == '0':
            exit(0)
        if data == '1':
            print('Balance: {}'.format(self.session_card.get_balance()))
        if data == '2':
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
        if not card.check_pin(self.session_pin):
            print('Wrong card number or PIN!')
            self.state = State.MAIN_MENU
            return
        print('You have successfully logged in!')
        self.session_card = card
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
