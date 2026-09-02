def calculate_total_expense(expenses):
    return sum(expenses)


def calculate_balance(income, total_expense):
    return income - total_expense


def generate_financial_advice(income, total_expense):
    balance = income - total_expense

    if balance > 0:
        return (
            f"Your remaining balance is ₹{balance:.2f}. "
            "Try to save a part of your remaining income."
        )
    elif balance == 0:
        return (
            "Your income and expenses are equal. "
            "Try to reduce unnecessary expenses."
        )
    else:
        return (
            "Your expenses are higher than your income. "
            "Consider reducing unnecessary spending."
        )