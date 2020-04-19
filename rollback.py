import sqlite3
import pytz
import datetime
import pickle

db = sqlite3.connect("accounts.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history(time TIMESTAMP NOT NULL,"
           " account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY(time, account))")
db.execute("CREATE VIEW IF NOT EXISTS localhistory AS "
           " SELECT strftime('%Y-%m-%d %H:%M:%f', history.time, 'localtime') AS localtime,"
           " history.account, history.amount FROM history ORDER BY history.time")


class Account(object):

    @staticmethod
    def _current_time():
         return pytz.utc.localize(datetime.datetime.utcnow())


    def __init__(self, name:str, opening_balance: int = 0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
        row = cursor.fetchone()
        if row is not None:
            self.name, self._balance = row
            print("Retrived record for {}. ".format(self.name), end='')
        else:
            self.name = name
            self._balance = opening_balance
            cursor.execute("INSERT INTO accounts VALUES(?, ?)",(name, opening_balance))
            cursor.connection.commit()
            print("Account created for {}.".format(self.name), end='')
        self.show_balance()

    def _sava_update(self, amount):
        new_balance =self._balance + amount
        transaction_time = Account._current_time() # <-- unpack return tuple
        try:
            db.execute("UPDATE accounts SET balance=? WHERE (name=?)",(new_balance, self.name))
            db.execute("INSERT INTO history VALUES(?, ?, ?, ?)", (transaction_time, self.name, amount))
        except sqlite3.Error:
            db.rollback()
        else:
            self._balance = new_balance
        finally:
            db.commit()
        self._balance = new_balance

    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            # new_balance = self._balance + amount
            # deposit_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance=? WHERE (name=?)",(new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
            # db.commit()
            # self._balance = new_balance
            self._sava_update(amount)
            # print("{:.2f} deposited".format(amount / 100))
        return self._balance

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            # new_balance =self._balance - amount
            # withdrawal_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance=? WHERE (name=?)",(new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (withdrawal_time, self.name, -amount))
            # db.commit()
            # self._balance = new_balance
            self._sava_update(-amount)
            # print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            # print("The amount must be greater than zero and no more than your account balance")
            return 0.0

    def show_balance(self):
        print("Balance on account {} is {:.2f} ".format(self.name, self._balance / 100))


if __name__ == '__main__':
    raj = Account('Raj')
    raj.deposit(1010)
    raj.deposit(10)
    raj.deposit(10)
    raj.withdraw(30)
    raj.withdraw(0)
    raj.show_balance()

    kiki = Account('kiki', 9000)
    pura = Account('pura')
    puki = Account('puki', 7000)
