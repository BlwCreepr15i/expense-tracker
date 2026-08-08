import tkinter as tk

class GUI:

    def __init__(self, title):

        self.root = tk.Tk()

        # Window Settings
        self.root.geometry("800x450")
        self.root.title(title)

        # Menus
        self.show_main_menu()

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

    def show_read_menu():
        pass

    def show_write_menu(): 
        pass

    def show_report_menu():
        pass

    


###################################################


GUI("Expense Tracker GUI")