from expense import Expense
from storage import ExpenseDatabase
from report import ExpenseReport

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
