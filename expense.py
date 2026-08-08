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
        
        if not self.is_year_valid(value.year):
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

    @classmethod
    def is_year_valid(cls, year : int):
        return year >= cls.YEAR_LOWER_LIMIT and year <= cls.YEAR_UPPER_LIMIT # both inclusive

    # returns the number of days apart (the day of timedelta)
    # if positive, then this date is in the future of other date;
    # if negative, then opposite of the above case; 
    def compare_date(self, other) -> int:
        if type(other) != Expense:
            raise NotImplementedError('Invalid type!')
        
        t_delta = self.date - other.date
        return t_delta.days

    def __str__(self):
        return f'{self._date.strftime('%m/%d/%Y')}, {self._category}, {self._amount}, {self._description}'
