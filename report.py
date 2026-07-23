from expense import Expense
from storage import ExpenseDatabase

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

