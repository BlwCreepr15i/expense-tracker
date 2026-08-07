import tkinter as tk

root = tk.Tk()

root.geometry("800x450")
root.title("Expense Tracker GUI")

title_label = tk.Label(root, text="Expense Tracker", font=("Arial", 20))
title_label.pack(padx=20, pady=20)

mode_label = tk.Label(root, text="Select mode:", font=("Arial", 12))
mode_label.pack(padx=5, pady=10)

button_frame = tk.Frame(root)
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

root.mainloop()