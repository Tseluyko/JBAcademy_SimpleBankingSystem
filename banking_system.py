from enum import Enum

from credit_card import CreditCard
from customer_storage import CustomerStorage
from menu_descriptions import *


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
        self.storage = CustomerStorage()
        self.state = State.MAIN_MENU
        self.session_card_number = ''
        self.transfer_dst = 0

    def get_menu(self):
        if self.state == State.MAIN_MENU:
            return get_main_menu()
        if self.state == State.IN_ACCOUNT:
            return get_user_menu()
        if self.state == State.ENTERING_NUMBER:
            return get_menu_number()
        if self.state == State.ENTERING_PIN:
            return get_menu_pin()
        if self.state == State.INCOMING:
            return get_menu_income()
        if self.state == State.TRANS_WELCOME:
            return get_menu_trans_welcome()
        if self.state == State.TRANS_MONEY:
            return get_menu_trans_money()

    def login_process(self):
        self.state = State.ENTERING_NUMBER

    def main_menu_processing(self, data):
        if data == '0':
            self.exit_process()
        if data == '1':
            self.emit_card_process()
        if data == '2':
            self.login_process()

    @staticmethod
    def exit_process():
        print("Bye!")
        exit(0)

    def emit_card_process(self):
        cn, pin = self.storage.add_new_customer()
        print('Your card has been created')
        print('Your card number:')
        print(cn)
        print('Your card PIN:')
        print(pin)

    def entering_number_processing(self, data):
        self.session_card_number = data
        self.state = State.ENTERING_PIN

    def entering_pin_processing(self, data):
        return self.checking_process(data)

    def checking_process(self, pin):
        card = self.storage.find_user(self.session_card_number)
        if not card:
            print('Wrong card number or PIN!')
            self.state = State.MAIN_MENU
            return
        if card[2] != pin:
            print('Wrong card number or PIN!')
            self.state = State.MAIN_MENU
            return
        print('You have successfully logged in!')
        self.state = State.IN_ACCOUNT

    def user_menu_processing(self, data):
        if data == '0':
            self.exit_process()
        if data == '1':
            self.balance_process()
        if data == '2':
            self.state = State.INCOMING
        if data == '3':
            self.state = State.TRANS_WELCOME
        if data == '4':
            self.delete_process()
        if data == '5':
            self.state = State.MAIN_MENU

    def balance_process(self):
        balance = self.storage.get_balance(self.session_card_number)
        print(f'Balance: {balance}')

    def delete_process(self):
        self.storage.delete_customer(self.session_card_number)
        print('The account has been closed!')
        self.session_card_number = None
        self.state = State.MAIN_MENU

    def income_processing(self, data):
        self.storage.income_money(self.session_card_number, int(data))
        self.state = State.IN_ACCOUNT

    def transfer_welcome_processing(self, data):
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

    def transfer_money_processing(self, data):
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
            return self.entering_number_processing(data)
        if self.state == State.ENTERING_PIN:
            return self.entering_pin_processing(data)
        if self.state == State.INCOMING:
            return self.income_processing(data)
        if self.state == State.TRANS_WELCOME:
            return self.transfer_welcome_processing(data)
        if self.state == State.TRANS_MONEY:
            return self.transfer_money_processing(data)
