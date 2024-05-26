def calculate_pf_contribution(age, salary):
    if salary <= 750:
        return "Salary must be greater than $750 to apply the contribution rates."
    
    # Define the contribution rates based on age groups
    contribution_rates = [
        (55, 17, 20, 37),
        (60, 15, 16, 31),
        (65, 11.5, 10.5, 22),
        (70, 9, 7.5, 16.5),
        (float('inf'), 7.5, 5, 12.5)
    ]
    
    # Find the applicable contribution rates
    for max_age, employer_rate, employee_rate, total_rate in contribution_rates:
        if age <= max_age:
            total_contribution = (total_rate / 100) * salary
            return total_rate
    
    return "Age is out of range for the given contribution rates."


