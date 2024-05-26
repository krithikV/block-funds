def calculate_overall_rating(monthly_income, monthly_expenses, solid_net_worth):
    """
    Calculate the overall rating on a scale of 1-5 based on monthly income, monthly expenses, and solid net worth.
    """
    # Calculate the savings rate (portion of income saved)
    savings_rate = (monthly_income - monthly_expenses) / monthly_income

    # Calculate the wealth ratio (net worth to annual income ratio)
    wealth_ratio = solid_net_worth / (12 * monthly_income)

    # Determine the overall rating based on savings rate and wealth ratio
    if savings_rate >= 0.5 and wealth_ratio >= 12:
        return 5
    elif savings_rate >= 0.3 and wealth_ratio >= 6:
        return 4
    elif savings_rate >= 0.2 and wealth_ratio >= 3:
        return 3
    elif savings_rate >= 0.1 and wealth_ratio >= 1:
        return 2
    else:
        return 1



