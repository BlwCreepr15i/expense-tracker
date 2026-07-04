from pathlib import Path
import re

FILENAME = 'expenses.csv'

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
        if re.match(r"^1?\d/[1-9]\d/[1-9]\d{3}$", date):
            month, day, year = date.split('/')
            if 1 <= int(month) <= 12 and 1 <= int(day) <= 31 and self.YEAR_LOWER_LIMIT <= year <= self.YEAR_UPPER_LIMIT:
                self._date = date
                return
            raise ValueError("Invalid or unsupported date input!")
        else:
            raise ValueError("Invalid date format!")
        
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @amount.setter
    def amount(self, value):
        self._amount = round(value, 2)

    @property
    def description(self) -> str:
        return self._description
    
    def __str__(self):
        return f"{self._date}, {self._category}, {self._amount}, {self._description}"


class ExpenseDatabase:
    def __init__(self, filename : str, parent_dir : str = "files"):
        self.path = Path(parent_dir + "/" + filename)
    
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
        with open(FILENAME, 'a') as file:
            file.write(f'\n{expense}')

    def __str__(self):
        with open(self._path, 'r') as file:
            data = file.read()
        return data

# ExpenseReport, CLI, etc.    
### Awaiting refactoring ###

def get_input():
    date = input('Date: ')
    cat = input('Category: ')
    amount = round(float(input('Amount($): ')), 2) # TBI try-except
    description = input('Description: ')
    return date, cat, amount, description

def check_date(date : str): # see Expense class date setter
        if re.match(r"^1?\d/[1-9]\d/[1-9]\d{3}$", date):
            month, day, _ = date.split('/')
            return 1 <= int(month) <= 12 and 1 <= int(day) <= 31
        return False

def init_file(): # see ExpenseDatabase class filename setter
    path = Path(FILENAME)
    if not path.exists():
        path.touch()
        path.write_text('Date, Category, Amount, Description')

def save_input(date, cat, amount, desc): # see ExpenseDatabase class add_expense method
    init_file()
    with open(FILENAME, 'a') as file:
        file.write(f'\n{date}, {cat}, {amount}, {desc}')

def print_all(): # see ExpenseDatabase class __str__ method
    if not Path(FILENAME).exists():
        print("Error: No record was found!")
        return
    with open(FILENAME, 'r') as file:
        data = file.read()
    print(data)

def print_report(month, year):

    print(f'----- Monthly report of {month}/{year} -----')
    with open(FILENAME, 'r') as file:
        headers = file.readline().strip()
        data = file.readlines()
    
    cats = {}
    total = 0
    all_records = ''
    for row in data:
        elements = [element.strip() for element in row.split(',')]
        mo, _, yr = elements[0].split('/')
        mo, yr = int(mo), int(yr) # bugfix

        if mo == month and yr == year:
            all_records += row # each row ends with \n
            cost = float(elements[2])
            total += cost
            if cats.get(elements[1]) == None:
                cats[elements[1]] = cost
            else:
                cats[elements[1]] += cost
    all_records += '\n'

    # Find category with most expenses
    max_cat = 'None'
    max_expense = 0
    for key in cats:
        if cats[key] >= max_expense:
            max_expense = cats[key]
            max_cat = key
    print(f'>> Total expense: ${total:.2f}')
    if total == 0 and max_expense == 0:
        print('>> Category with the most expense: None\n')
        return
    percentage = max_expense / total * 100
    print(f'>> Category with the most expense: {max_cat} - ${max_expense} ({percentage:.1f}%)\n')
    
    # Category breakdown
    print('Category Full Breakdown:')
    for key in cats:
        print(f'>> {key} - ${cats[key]} ({cats[key]/total*100:.1f}%)')
    print()

    # Show all records upon requested
    show_records = bool(input('Would you like to see more details? (True/False): '))
    if show_records:
        print(f'Here is all entries ({month}/{year}): ') 
        print(all_records)

def main():
    while True:
        mode = input('Select modes (read/write/report): ').upper().strip()
        match mode:
            case 'READ':
                print()
                print_all()
                print()
                break
            case 'REPORT':
                try:
                    month = int(input('Of which month (1-12): '))
                    year = int(input('Of which year: '))
                    if month < 1 or month > 12 or year < 1000 or year > 9999:
                        raise ValueError()
                except ValueError:
                    print('Error: Invalid or unsupported month/year input!')
                    continue # very inconvenient, user forced to re-enter mode (FIXME)
                else:
                    print_report(month, year)
                    break
            case 'WRITE':
                inputs = list(get_input())
                while not check_date(inputs[0]):
                    print('\nError: Invalid date!')
                    inputs[0] = input('Enter a new date (mm/dd/yyyy): ')
                save_input(*inputs)
                print('Saving...')
                break
            case _:
                print('Invalid mode!')

if __name__ == '__main__':
    main()