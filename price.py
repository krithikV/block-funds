import pandas as pd
import datetime

# Load inflation rates dataset from CSV
df = pd.read_csv('inflation_rate_f_25.csv')
df['ds'] = pd.to_datetime(df['ds'])
df.set_index('ds', inplace=True)

# Initial household expense (assuming current prices)
current_expenses = { 
    "Food": 755.5, 
    "Clothing & Footwear": 113, 
    "Housing & Utilities": 426, 
    "Household Durables & Services": 282, 
    "Health Care": 172, 
    "Transport": 476, 
    "Communication": 240, 
    "Recreation & Culture": 225, 
    "Miscellaneous Goods & Services": 501 
} 

# Function to estimate future expense for a specific month and year
def estimate_expense(utility, year, month, current_year=datetime.datetime.now().year, current_month=5):
    # Calculate the cumulative inflation rate for the utility up to the target month and year
    if int(year) < int(datetime.datetime.now().year):
        raise ValueError(f"Enter a year more than {datetime.datetime.now().year}")

    if utility not in current_expenses:
        raise ValueError(f"Utility '{utility}' not found in current expenses.")
    
    col_name = f"{utility.replace(' ', '_')}_yhat"
    if col_name not in df.columns:
        raise ValueError(f"Utility '{utility}' not found in inflation data.")
    
    current_price = current_expenses[utility]
    inflation_data = df[col_name]
    
    # Get the relevant inflation rates
    start_date = pd.Timestamp(year=current_year, month=current_month, day=1)
    end_date = pd.Timestamp(year=year, month=month, day=1)
    relevant_inflation_data = inflation_data[start_date:end_date]
    
    # Calculate cumulative inflation rate
    cumulative_inflation_rate = (1 + relevant_inflation_data / 100).prod() - 1
    
    # Cap the inflation rate at +100% or -100%
    # if cumulative_inflation_rate > 1:
    #     cumulative_inflation_rate = 1
    # elif cumulative_inflation_rate < -1:
    #     cumulative_inflation_rate = -1
    
    # Adjust the current price to the target month and year price
    estimated_price = current_price * (1 + cumulative_inflation_rate)
    
    return estimated_price

# Function to calculate the best and worst future months
def best_worst_months(utility, current_year=2023, current_month=5):
    col_name = f"{utility.replace(' ', '_')}_yhat"
    if col_name not in df.columns:
        raise ValueError(f"Utility '{utility}' not found in the dataset.")
    
    inflation_data = df[col_name]
    # Filter out past months
    start_date = pd.Timestamp(year=current_year, month=current_month, day=1)
    future_inflation_data = inflation_data[inflation_data.index > start_date]
    
    # Resample monthly inflation data to monthly periods
    monthly_inflation = future_inflation_data.resample('ME').sum()
    
    best_month = monthly_inflation.idxmin()
    worst_month = monthly_inflation.idxmax()
    best_rate = monthly_inflation.min()
    worst_rate = monthly_inflation.max()
    
    return {
        "best_month": best_month.strftime('%Y-%m'),
        "best_rate": best_rate,
        "worst_month": worst_month.strftime('%Y-%m'),
        "worst_rate": worst_rate
    }

# Example usage:
utility_name = "Food"
target_year = 2026
target_month = 1

estimated_expense = estimate_expense(utility_name, target_year, target_month)
print(f"Estimated expense for {utility_name} in {target_year}-{target_month:02d}: ${estimated_expense:.2f}")

best_worst = best_worst_months(utility_name)
print(f"Best month for {utility_name}: {best_worst['best_month']} with rate {best_worst['best_rate']:.2f}%")
print(f"Worst month for {utility_name}: {best_worst['worst_month']} with rate {best_worst['worst_rate']:.2f}%")
