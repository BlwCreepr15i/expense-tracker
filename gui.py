import tkinter as tk
from tkinter import ttk

from expense import Expense
from storage import ExpenseDatabase

class GUI:

    def __init__(self, title, db_name="expenses"):

        self.db = ExpenseDatabase(db_name)
        self.root = tk.Tk()

        # Window Settings
        self.root.geometry("800x450")
        self.root.title(title)

        # Menus
        # self.show_main_menu()
        self.show_read_menu()
        # self.show_write_menu()
        # self.show_report_menu()

        self.root.mainloop()
    
    def show_main_menu(self):
        title_label = tk.Label(self.root, text="Expense Tracker", font=("Arial", 20))
        title_label.pack(padx=20, pady=20)
        
        mode_label = tk.Label(self.root, text="Select mode:", font=("Arial", 12))
        mode_label.pack(padx=5, pady=10)

        # Button frame from mode selection
        button_frame = tk.Frame(self.root)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        read_button = tk.Button(button_frame, text="Read", font=("Arial", 14))
        read_button.grid(row=0, column=0)
        
        write_button = tk.Button(button_frame, text="Write", font=("Arial", 14))
        write_button.grid(row=0, column=1)
        
        report_button = tk.Button(button_frame, text="Report", font=("Arial", 14))
        report_button.grid(row=0, column=2)
        
        button_frame.pack(pady=10, fill='x')

    def show_read_menu(self):
        title_label = tk.Label(self.root, text="Expense Tracker (Mode: Reading)", font=("Arial", 12))
        title_label.grid(row=0, column=0, sticky="w")

        # Month/year frame
        frame = tk.Frame(self.root)
        frame.grid(row=1, column=0, sticky="new", padx=20, pady=10)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=2)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        month_label = tk.Label(frame, text="Which month would you want to see?", font=("Arial", 12))
        month_label.grid(row=0, column=0, sticky="ew", pady=6)

        month_options = ("All month", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        month_drop_selected = tk.StringVar()
        month_drop_selected.set(month_options[0])

        month_drop = ttk.OptionMenu(frame, month_drop_selected, *month_options)
        month_drop.grid(row=0, column=1)

        year_label = tk.Label(frame, text="Which year would you want to see?", font=("Arial", 12))
        year_label.grid(row=1, column=0, sticky="ew", pady=6)

        year_input = tk.Entry(frame)
        year_input.grid(row=1, column=1)

        all_year_check_var = tk.BooleanVar()
        all_year_check = tk.Checkbutton(frame, text="I want to see all data.", variable=all_year_check_var)
        all_year_check.grid(row=2, column=1)
        
        show_button = tk.Button(frame, text="Show data", command=lambda: 
                                self.show_data(all_year_check_var.get(), year_input, month_options.index(month_drop_selected.get())))
        show_button.grid(row=2, column=0)

        
    def show_data(self, show_all : bool, year_input : tk.Entry, month : int):

        error_label = tk.Label(self.root, text="\t\t\t", padx=10, pady=10)
        error_label.grid(row=2, column=0, sticky="nw", columnspan=2)
        self.root.rowconfigure(2, weight=1)
        
        # Frame for display
        data_frame = tk.Frame(self.root)
        data_frame.grid(row=3, column=0, sticky="nsew")
        data_frame.rowconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=2)
        data_frame.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

        data_list = tk.Listbox(data_frame)
        data_list.grid(row=1, column=0, columnspan=2, sticky="nsew")

        if show_all:
            data_list.delete(0, tk.END)  

            for expense in self.db.get_all_expenses():
                data_list.insert(0, str(expense))
            return

        # error checking
        try:
            year = int(year_input.get())
            year_input.delete(0, tk.END)
        except ValueError:
            error_label.config(text="Error: Invalid Year!\t\t", font=("Arial", 10))
            return
        else:
            if not Expense.is_year_valid(year):
                error_label.config(text="Error: Unsupported Year!", font=("Arial", 10))
                return

        data_list.delete(0, tk.END)
        
        if month == 0:
            # show year data
            ... # TBI
        else:
            # show month-year data
            ... # TBI

    def show_write_menu(self): 
        pass # TBI

    def show_report_menu(self):
        pass # TBI


###################################################

GUI("Expense Tracker GUI")