from time import sleep
from random import randint
from threading import Thread, Lock


class Bank:
    def __init__(self, balance: int = 0, lock: Lock = Lock()):
        self.balance = balance
        self.lock = lock

    def deposit(self):
        for i in range(100):
            replenishment = randint(50, 500)
            self.balance += replenishment
            print(f'Пополнение: {replenishment}. Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            sleep(0.001)

    def take(self):
        for i in range(100):
            withdrawals = randint(50, 500)
            print(f'Запрос на {withdrawals}')
            if withdrawals <= self.balance:
                self.balance -= withdrawals
                print(f'Снятие: {withdrawals}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()


bk = Bank()
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))
th1.start()
th2.start()
th1.join()
th2.join()
print(f'Итоговый баланс: {bk.balance}')
