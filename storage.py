import sqlite3

from expense import Expense

class ExpenseDatabase:

    def __init__(self, name : str):
        self.name = name
        self.conn = sqlite3.connect(name + '.db')
        self.cursor = self.conn.cursor()

    def add_expense():
        ... # TBI

    def get_all_expenses():
        ... # TBI

    def __str__(self):
        ... # TBI