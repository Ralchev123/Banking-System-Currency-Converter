from tkinter import Tk, ttk, Button, Entry, Frame, Label, Toplevel, LEFT, messagebox
import requests
import json
import os
from tkinter import *

cor0 = "#FFFFFF"
cor1 = "#333333"
cor2 = "#FFA500"


class AccountManager:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name):
        if name in self.accounts:
            messagebox.showerror("Error", "An account with that name already exists.")
        else:
            self.accounts[name] = 0
            self.save_account_balance(name)

    def save_account_balance(self, name):
        balance = self.accounts[name]
        filename = f"{name}_balance.txt"
        with open(filename, "w") as file:
            file.write(str(balance))

    def delete_account(self, name):
        if name in self.accounts:
            del self.accounts[name]
            self.delete_account_balance_file(name)
            messagebox.showinfo("Success", "Account deleted successfully.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def delete_account_balance_file(self, name):
        filename = f"{name}_balance.txt"
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def load_account_balance(self, name):
        filename = f"{name}_balance.txt"
        try:
            with open(filename, "r") as file:
                balance = float(file.read())
                self.accounts[name] = balance
        except FileNotFoundError:
            self.accounts[name] = 0


def open_account_window():
    def open_new_account():
        name = name_entry.get()
        account_manager.create_account(name)
        name_entry.delete(0, "end")

    account_window = Toplevel()
    account_window.geometry("300x200")
    account_window.title("Open Account")
    account_window.resizable(height=False, width=False)

    name_label = ttk.Label(account_window, text="Account Name:")
    name_label.place(x=50, y=50)

    name_entry = ttk.Entry(account_window, width=20)
    name_entry.place(x=50, y=80)
    name_entry.focus()

    open_button = ttk.Button(
        account_window, text="Open Account", command=open_new_account
    )
    open_button.place(x=50, y=120)


def open_banking_window():
    def start_banking():
        account_name = name_entry.get()
        banking_window.destroy()
        banking(account_name)

    banking_window = Toplevel()
    banking_window.geometry("300x200")
    banking_window.title("Banking")
    banking_window.resizable(height=False, width=False)

    name_label = ttk.Label(banking_window, text="Account Name:")
    name_label.place(x=50, y=50)

    name_entry = ttk.Entry(banking_window, width=20)
    name_entry.place(x=50, y=80)
    name_entry.focus()

    start_button = ttk.Button(
        banking_window, text="Start Banking", command=start_banking
    )
    start_button.place(x=50, y=120)


def banking(account_name):
    class Bank:
        def __init__(self, name):
            self.name = name
            self.balance = self.load_balance(name)

        def load_balance(self, name):
            try:
                with open(f"{name}_balance.txt", "r") as file:
                    balance = float(file.read())
                    return balance
            except FileNotFoundError:
                return 0

        def save_balance(self, name):
            with open(f"{name}_balance.txt", "w") as file:
                file.write(str(self.balance))

        def deposit(self, amount):
            self.balance += amount
            self.save_balance(self.name)

        def withdraw(self, amount):
            if self.balance >= amount:
                self.balance -= amount
                self.save_balance(self.name)

    def deposit_money():
        amount = float(deposit_entry.get())
        bank.deposit(amount)
        balance_label.configure(text=f"Balance: ${bank.balance:.2f}")
        deposit_entry.delete(0, "end")

    def withdraw_money():
        amount = float(withdraw_entry.get())
        bank.withdraw(amount)
        balance_label.configure(text=f"Balance: ${bank.balance:.2f}")
        withdraw_entry.delete(0, "end")

    window2 = Tk()
    window2.geometry("400x200")
    window2.title("Banking System")
    window2.resizable(height=False, width=False)

    account_manager = AccountManager()

    account_manager.load_account_balance(account_name)

    bank = Bank(account_name)

    balance_label = ttk.Label(window2, text=f"Balance: ${bank.balance:.2f}")
    balance_label.pack(pady=10)

    deposit_frame = ttk.Frame(window2)
    deposit_frame.pack(pady=10)

    deposit_label = ttk.Label(deposit_frame, text="Deposit Amount:")
    deposit_label.grid(row=0, column=0)

    deposit_entry = ttk.Entry(deposit_frame)
    deposit_entry.grid(row=0, column=1)

    deposit_button = ttk.Button(deposit_frame, text="Deposit", command=deposit_money)
    deposit_button.grid(row=0, column=2, padx=10)

    withdraw_frame = ttk.Frame(window2)
    withdraw_frame.pack(pady=10)

    withdraw_label = ttk.Label(withdraw_frame, text="Withdraw Amount:")
    withdraw_label.grid(row=0, column=0)

    withdraw_entry = ttk.Entry(withdraw_frame)
    withdraw_entry.grid(row=0, column=1)

    withdraw_button = ttk.Button(
        withdraw_frame, text="Withdraw", command=withdraw_money
    )
    withdraw_button.grid(row=0, column=2, padx=10)

    window2.mainloop()


def delete_account_window():
    def delete_account():
        account_name = name_entry.get()
        account_manager.delete_account(account_name)
        delete_window.destroy()

    delete_window = Toplevel()
    delete_window.geometry("300x200")
    delete_window.title("Delete Account")
    delete_window.resizable(height=False, width=False)

    name_label = ttk.Label(delete_window, text="Account Name:")
    name_label.place(x=50, y=50)

    name_entry = ttk.Entry(delete_window, width=20)
    name_entry.place(x=50, y=80)
    name_entry.focus()

    delete_button = ttk.Button(
        delete_window, text="Delete Account", command=delete_account
    )
    delete_button.place(x=50, y=120)


def converter():
    window1 = Toplevel()
    window1.geometry("500x600")
    window1.title("Currency exchanger")
    window1.configure(bg=cor0)
    window1.resizable(height=False, width=False)

    top = Frame(window1, width=500, height=100, bg="#FFA500")
    top.grid(row=0, column=0)

    main = Frame(window1, width=300, height=300, bg=cor0)
    main.grid(row=1, column=0)

    def convert():
        url = "https://currency-converter18.p.rapidapi.com/api/v1/convert"

        currency1 = combo1.get()
        currency2 = combo2.get()
        amount = value.get()

        querystring = {"from": currency1, "to": currency2, "amount": amount}

        headers = {
            "X-RapidAPI-Key": "8379f85432msh00aae22a1b25efdp1638f8jsn86212058e478",
            "X-RapidAPI-Host": "currency-converter18.p.rapidapi.com",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)

        converted_amount = data["result"]["convertedAmount"]

        formatted = "{:,.2f}".format(converted_amount)

        result["text"] = formatted

        print(converted_amount, formatted)

    app_name = Label(
        top,
        text="Currency Converter",
        height=10,
        padx=13,
        pady=30,
        anchor=CENTER,
        font=("Arial 30 bold"),
        bg="#FFA500",
        fg=cor1,
    )
    app_name.place(x=0, y=0)

    result = Label(
        main,
        text="",
        width=16,
        height=2,
        pady=30,
        relief="solid",
        anchor=CENTER,
        font=("Ivy 15 bold"),
        bg=cor0,
        fg=cor1,
    )
    result.place(x=40, y=20)

    currency = ["USD", "BGN", "EUR", "GBP", "CAD"]

    from_label = Label(
        main,
        text="From",
        width=5,
        height=2,
        padx=0,
        pady=0,
        relief="flat",
        anchor=NW,
        font=("Ivy 10 bold"),
        bg=cor0,
        fg=cor1,
    )
    from_label.place(x=55, y=150)
    combo1 = ttk.Combobox(main, width=5, justify=CENTER, font=("Ivy 12 bold"))
    combo1["values"] = currency
    combo1.place(x=55, y=170)

    to_label = Label(
        main,
        text="To",
        width=5,
        height=2,
        padx=0,
        pady=0,
        relief="flat",
        anchor=NW,
        font=("Ivy 10 bold"),
        bg=cor0,
        fg=cor1,
    )
    to_label.place(x=170, y=150)
    combo2 = ttk.Combobox(main, width=5, justify=CENTER, font=("Ivy 12 bold"))
    combo2["values"] = currency
    combo2.place(x=170, y=170)

    value = Entry(main, width=20, justify=CENTER, font=("Ivy 12 bold"))
    value.place(x=40, y=210)

    button = Button(
        main,
        text="Convert",
        width=19,
        padx=5,
        height=1,
        bg=cor2,
        fg=cor0,
        font=("Ivy 12 bold"),
        command=convert,
    )
    button.place(x=50, y=270)


window = Tk()
window.geometry("500x600")
window.title("Menu")
window.resizable(height=False, width=False)

top1 = Frame(window, width=500, height=100, bg="#FFA500")
top1.grid(row=0, column=0)

text = Label(
    top1,
    text="Menu",
    width=20,
    padx=10,
    height=5,
    bg="#333333",
    fg="#FFFFFF",
    font=("Ivy 12 bold"),
)
text.place(x=135, y=20)

main1 = Frame(window, width=300, height=300, bg="#FFFFFF")
main1.grid(row=1, column=0)

button1 = Button(
    main1,
    text="Converter",
    width=19,
    padx=5,
    height=1,
    bg="#333333",
    fg="#FFFFFF",
    font=("Ivy 12 bold"),
    command=converter,
)
button1.place(x=50, y=60)

button2 = Button(
    main1,
    text="Banking",
    width=19,
    padx=5,
    height=1,
    bg="#333333",
    fg="#FFFFFF",
    font=("Ivy 12 bold"),
    command=open_banking_window,
)
button2.place(x=50, y=200)

button3 = Button(
    main1,
    text="Open new account",
    width=19,
    padx=5,
    height=1,
    bg="#333333",
    fg="#FFFFFF",
    font=("Ivy 12 bold"),
    command=open_account_window,
)
button3.place(x=50, y=130)

button4 = Button(
    main1,
    text="Delete account",
    width=19,
    padx=5,
    height=1,
    bg="#333333",
    fg="#FFFFFF",
    font=("Ivy 12 bold"),
    command=delete_account_window,
)
button4.place(x=50, y=270)

account_manager = AccountManager()

window.mainloop()
