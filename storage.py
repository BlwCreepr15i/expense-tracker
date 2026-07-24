import sqlite3

from expense import Expense

class ExpenseDatabase:

    def __init__(self, name : str):
        self.name = name
        self.conn = sqlite3.connect(name + '.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    @property
    def conn(self) -> sqlite3.Connection:
        return self._conn
    
    @conn.setter
    def conn(self, value : sqlite3.Connection):
        self._conn = value

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self._cursor
    
    @cursor.setter
    def cursor(self, value : sqlite3.Cursor):
        self._cursor = value

    def create_table(self):
        try:
            self._cursor.execute('''CREATE TABLE expenses (
                                    date text,
                                    category text,
                                    amount real
                                    )''')
            self._conn.commit()
        except sqlite3.OperationalError:
            pass

    def add_expense():
        ... # TBI

    def get_all_expenses():
        ... # TBI

    def __str__(self):
        ... # TBI