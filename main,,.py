import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

balance = 0

def update_balance():
    balance_label.config(text=f"Current Balance: ৳{balance}")

def add_income():
    global balance
    try:
        income = float(income_entry.get())
        balance += income
        update_balance()
        income_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid", "Enter a valid number")

def add_expense():
    global balance
    try:
        expense = float(expense_entry.get())
        if expense > balance:
            messagebox.showwarning("Warning", "Not enough balance!")
        else:
            balance -= expense
            update_balance()
        expense_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid", "Enter a valid number")

# App GUI
root = tk.Tk()
root.title("Money Manager")
root.geometry("400x500")
root.configure(bg="#005f73")

# Load Taka Icon
try:
    taka_img = Image.open("taka.png")
    taka_img = taka_img.resize((80, 80))
    taka_photo = ImageTk.PhotoImage(taka_img)
    icon_label = tk.Label(root, image=taka_photo, bg="#005f73")
    icon_label.pack(pady=10)
except:
    print("taka.png not found!")

# Title
title = tk.Label(root, text="Money Manager", font=("Helvetica", 24, "bold"), fg="white", bg="#005f73")
title.pack()

balance_label = tk.Label(root, text="Current Balance: ৳0", font=("Arial", 16), fg="white", bg="#005f73")
balance_label.pack(pady=10)

# Income section
tk.Label(root, text="Add Income:", font=("Arial", 12), bg="#005f73", fg="white").pack(pady=(10, 0))
income_entry = tk.Entry(root, font=("Arial", 12))
income_entry.pack(pady=5)
tk.Button(root, text="Add Income", bg="#ffb703", fg="black", font=("Arial", 12, "bold"), command=add_income).pack(pady=5)

# Expense section
tk.Label(root, text="Add Expense:", font=("Arial", 12), bg="#005f73", fg="white").pack(pady=(15, 0))
expense_entry = tk.Entry(root, font=("Arial", 12))
expense_entry.pack(pady=5)
tk.Button(root, text="Add Expense", bg="#e63946", fg="white", font=("Arial", 12, "bold"), command=add_expense).pack(pady=5)

root.mainloop()
