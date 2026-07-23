from pathlib import Path

from expense import Expense

class ExpenseDatabase:
    def __init__(self, filename : str, parent_dir : str = 'files'):
        self.path = Path(parent_dir + '/' + filename)
    
    @property
    def path(self) -> Path:
        return self._path
    
    @path.setter
    def path(self, value : Path):
        if not value.exists():
            value.parent.mkdir(exist_ok=True, parents=True)
            value.touch()
            value.write_text('Date, Category, Amount, Description')
        self._path = value
    
    def add_expense(self, expense : Expense):
        with open(self._path, 'a') as file:
            file.write(f'\n{expense}')
    
    def get_all_expenses(self) -> list[Expense]:
        with open(self._path, 'r') as file:
            file.readline()
            data = file.readlines()

        expenses = []
        for row in data:
            elements = [element.strip() for element in row.split(',')] # date, category, amount, desc
            elements[2] = float(elements[2]) # amount type conversion
            expenses.append(Expense(*elements))
        return expenses
    
    def __str__(self):
        with open(self._path, 'r') as file:
            data = file.read()
        return data

