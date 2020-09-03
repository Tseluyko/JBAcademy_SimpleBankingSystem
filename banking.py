from banking_system import BankSystem

bank = BankSystem()

while True:
    bank.input_processing(input(bank.get_menu()))
