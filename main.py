from pathlib import Path
import re

class Expense:

    YEAR_LOWER_LIMIT = 1930
    YEAR_UPPER_LIMIT = 2999

    def __init__(self, date : str, category : str, amount : float, desc : str):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = desc
    
    @property
    def date(self) -> str:
        return self._date
    
    @date.setter
    def date(self, date : str):
        if re.match(r'^1?\d/[1-9]\d/[1-9]\d{3}$', date):
            month, day, year = date.split('/')
            if 1 <= int(month) <= 12 and 1 <= int(day) <= 31 and self.YEAR_LOWER_LIMIT <= int(year) <= self.YEAR_UPPER_LIMIT:
                self._date = date
                return
            raise ValueError('Invalid or unsupported date input!')
        else:
            raise ValueError('Invalid date format!')
        
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @amount.setter
    def amount(self, value : float):
        self._amount = round(value, 2)

    @property
    def description(self) -> str:
        return self._description
    
    def __str__(self):
        return f'{self._date}, {self._category}, {self._amount}, {self._description}'


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

    def __str__(self):
        with open(self._path, 'r') as file:
            data = file.read()
        return data


class ExpenseReport:
    def __init__(self, database : ExpenseDatabase):
        self.database = database
    
    @property
    def database(self) -> ExpenseDatabase:
        return self._database
    
    @database.setter
    def database(self, value : ExpenseDatabase):
        self._database = value

    @staticmethod
    def find_max(cat_costs : dict) -> tuple[str, float]:
        max_cat = 'None'
        max_expense = 0
        for key in cat_costs:
            if cat_costs[key] >= max_expense:
                max_expense = cat_costs[key]
                max_cat = key
        return max_cat, max_expense
    
    def print_report(self, month : int, year : int):
        if month < 1 or month > 12 or year < Expense.YEAR_LOWER_LIMIT or year > Expense.YEAR_UPPER_LIMIT:
            raise ValueError('Invalid or unsupported month/year input')
        
        print(f'----- Monthly report of {month}/{year} -----')
        with open(self._database.path, 'r') as file:
            file.readline().strip() # skips the headers/ column titles
            data = file.readlines()

        cats = {}
        total = 0
        all_records = ''
        for row in data:
            elements = [element.strip() for element in row.split(',')]
            mo, _, yr = elements[0].split('/')
            mo, yr = int(mo), int(yr)

            if mo == month and yr == year:
                all_records += row # each row ends with \n
                cost = float(elements[2])
                total += cost
                if cats.get(elements[1]) == None:
                    cats[elements[1]] = cost
                else:
                    cats[elements[1]] += cost
        all_records += '\n'

        max_cat, max_expense = self.find_max(cats)
        if total == 0:
            percentage = 0 # prevents division by zero errors
        else:
            percentage = max_expense / total * 100

        print(f'>> Total expense: ${total:.2f}')
        print(f'>> Category with the most expense: {max_cat} - ${max_expense} ({percentage:.1f}%)\n')

        if total != 0:
            breakdown = 'Category Full Breakdown:\n'
            for key in cats:
                breakdown += f'>> {key} - ${cats[key]} ({cats[key]/total*100:.1f}%)\n'
            print(breakdown)


class CLI:
    def __init__(self, filename):
        self.exp_db = ExpenseDatabase(filename)
        self.activate()

    def activate(self):
        while True:
            mode = input('Select modes (read/write/report): ').upper().strip()
            match mode:
                case 'READ':
                    self.read_mode()
                    break
                case 'REPORT':
                    if self.report_mode():
                        break
                case 'WRITE':
                    if self.write_mode():
                        break
                case _:
                    print('Invalid mode!')
    
    def read_mode(self):
        print(self.exp_db)

    def write_mode(self) -> bool:
        try:
            expense = Expense(*self.get_input())
        except ValueError:
            print('Invalid or unsupported input!')
            return False
        
        self.exp_db.add_expense(expense)
        print('Saving...')
        return True

    def report_mode(self) -> bool:
        try:
            month = int(input('Of which month (1-12): '))
            year = int(input('Of which year: '))
        except ValueError:
            print('Error: Invalid inputs')
            return False
        report = ExpenseReport(self.exp_db)
        try:
            report.print_report(month, year)
            return True
        except ValueError:
            print('Error: Invalid or unsupported month / year formats')
            return False

    def get_input(self) -> tuple[str, str, float, str]:
        date = input('Date: ')
        cat = input('Category: ')
        amount = round(float(input('Amount($): ')), 2)
        description = input('Description: ')
        return date, cat, amount, description

def main():
    CLI('expenses.csv')

if __name__ == '__main__':
    main()