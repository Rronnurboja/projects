from datetime import datetime

date_format = "%d-%m-%Y" # this is the date format we want
CATEGORIES = {"I":"Income","E":"Expense"}  # a dict for our prompt later

def get_date(prompt, allow_default=False):  # this allow_default parameter shall mean that by default, you get returned today's date
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)   # i think this means date plus time, meaning the prompt date should be of this format??
        return valid_date.strftime(date_format)  # 'string format time' formats how the date should be
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)  # this will return a reprompt basically

def get_amount():
    try:
        amount = float(input("Enter the amount of money: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()  # again reprompt

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]  # will return 'Income' or 'Expense' from the DICT
    else:
        print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
        return get_category()

def get_description():
    description = input("Enter a description (optional): ")
    return description


