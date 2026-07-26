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
                                    amount real,
                                    description text
                                    )''')
            self._conn.commit()
        except sqlite3.OperationalError:
            pass

    def add_expense(self, expense : Expense):
        with self._conn:
            self._cursor.execute('INSERT INTO expenses VALUES (?, ?, ?, ?)', 
                             (expense.date.strftime('%m/%d/%Y'), expense.category, expense.amount, expense.description))

    def get_all_expenses(self) -> list[Expense]:
        with self._conn:
            self._cursor.execute('SELECT * FROM expenses')
            all_data = self._cursor.fetchall()

        expenses = []
        for row in all_data:
            expenses.append(Expense(*row))
        return expenses

    def __str__(self):
        data_str = 'Date, Category, Amount, Description\n'
        expenses = self.get_all_expenses()

        for expense in expenses:
            data_str += str(expense) + '\n'
        return data_str