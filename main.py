from pathlib import Path
import datetime

class Expense:

    YEAR_LOWER_LIMIT = 1930
    YEAR_UPPER_LIMIT = 2999

    def __init__(self, date : str, category : str, amount : float, desc : str):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = desc
    
    @property
    def date(self) -> datetime.date:
        return self._date
    
    @date.setter
    def date(self, value : str):
        try:
            value = datetime.datetime.strptime(value, '%m/%d/%Y').date()
        except ValueError:
            raise ValueError('Invalid date.')
        
        if value.year < self.YEAR_LOWER_LIMIT or value.year > self.YEAR_UPPER_LIMIT:
            raise ValueError('Unsupported date year.')
        self._date = value
        
    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, value : str):
        self._category = value

    @property
    def amount(self) -> float:
        return self._amount
    
    @amount.setter
    def amount(self, value : float):
        self._amount = round(value, 2)

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value : str):
        self._description = value
    
    def __str__(self):
        return f'{self._date.strftime('%m/%d/%Y')}, {self._category}, {self._amount}, {self._description}'


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

        cats = {}
        total = 0
        all_records = ''
        for expense in self._database.get_all_expenses():

            date = expense.date
            if date.month == month and date.year == year:
                all_records += str(expense) + '\n'
                cost = expense.amount
                total += cost
                if cats.get(expense.category) == None:
                    cats[expense.category] = cost
                else:
                    cats[expense.category] += cost

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
        except ValueError as e:
            print(e)
            return False
        
        self.exp_db.add_expense(expense)
        print('Saving...')
        return True

    def report_mode(self) -> bool:
        try:
            month = int(input('Of which month (1-12): '))
            year = int(input('Of which year: '))
        except ValueError as e:
            print('Error: Invalid inputs')
            return False
        report = ExpenseReport(self.exp_db)
        try:
            report.print_report(month, year)
            return True
        except ValueError as e:
            print(e)
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