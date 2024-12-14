import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1|2|3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transaction(start_date, end_date)
            while True:
                plot_choice = input("Do you want to see a plot? (y/n) ").lower()
                if plot_choice == "y":
                    plot_transactions(df)
                    break
                elif plot_choice == "n":
                    print("OK. No plot then.")
                    break
                else:
                    print("Please write 'y' or 'n': ")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")
class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):  # don't forget that the first parameter is supposed to add to the class
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)  # to include stuff from outside the class, you need to to do it using the parameter cls, in our case
            df.to_csv(cls.CSV_FILE, index=False)   # the reason we did this by using a try-except blockage is so we don't get to create the csv file more than once

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {    # created a dict
            "date": date,          # don't forget that in python the name of the variable (or dict or whatever) comes first, then the value (meaning the date parameter will be stored to the csv column 'date' as the value that will be given later)
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:  # we opened the file in append mode (we can append entries). It also handles closing the file for us
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)     # we write into the dict, where the field names are COLUMNS
            writer.writerow(new_entry)     # within 'writer', write the rows with the new_entry data
        print("Entry added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date): # transactions have a start and end
        df = pd.read_csv(cls.CSV_FILE)  # our dataframe
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)  # we have converted our dataframe (["date"] column) into an object so we can use them to filter by transactions
        start_date = datetime.strptime(start_date, CSV.FORMAT)   # the start date is going to be given as a string, therefore we need to put it in correct format
        end_date = datetime.strptime(end_date, CSV.FORMAT)    # same here

        mask = (df["date"] >= start_date) & (df["date"] <= end_date) # this is the filtering part and '&' is required in pandas apparently and also we are constantly checking that the date of transactions is logical (makes sense)
        filtered_df = df.loc[mask]  # filtering the df into the rows where the mask applies

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)})) # the parameter 'x' is going to be a date_time object which we format to string now # don't forget the mask above will deal with ints (as it compares obv) therefore we need to convert our data into string
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income-total_expense):.2f}")

        return filtered_df # return so we may be able to use it in a plot or graph

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or press 'enter' for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)  # obv, parameters

def plot_transactions(df):
    df.set_index('date', inplace=True)  # we want to find the correct information based on the date and then create the plot

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0) # the D stands for daily frequency (basically if you have a transaction after 4 days, the plot line will go along the days)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
