# Feature 6: Simple Expiry Check (Date-based)
#
# This module handles simple expiry checking by comparing dates:
# - Check which ingredients have expired
# - Remove expired ingredients automatically
# - Show expiry status of all ingredients
# - Simple date comparison (no ML)
#
# Uses concepts from syllabus:
# - Pandas for CSV operations
# - Datetime for date handling and comparison
# - Boolean indexing for filtering
# - Conditional statements

# Import required libraries (all from syllabus)
import pandas as pd  # For CSV operations and data manipulation
from datetime import datetime  # For date handling and comparison
import os  # For file path operations

def get_data_file_path(filename):
    # Get the correct path to data files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_path = os.path.join(parent_dir, "data", filename)

    # If data directory doesn't exist, create it
    data_dir = os.path.dirname(data_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_path

def load_ingredients():
    # Load ingredients from CSV file
    # Returns: pandas DataFrame with ingredients data
    try:
        # Read ingredients CSV file using correct path
        ingredients_file = get_data_file_path("ingredients.csv")
        ingredients_df = pd.read_csv(ingredients_file)
        return ingredients_df
    except FileNotFoundError:
        print(" Ingredients file not found.")
        return pd.DataFrame()

def save_ingredients(df):
    # Save ingredients DataFrame to CSV file
    # Args: df (pandas DataFrame) - ingredients data to save
    try:
        ingredients_file = get_data_file_path("ingredients.csv")
        df.to_csv(ingredients_file, index=False)
    except Exception as e:
        print(f" Error saving ingredients: {e}")

def check_expiry_simple():
    # Check expiry status of all ingredients using simple date comparison
    # This function demonstrates date operations and conditional logic
    # 
    # Uses syllabus concepts:
    # - Pandas read_csv() and DataFrame operations
    # - Datetime operations and date comparison
    # - Boolean indexing for filtering
    # - For loops and conditional statements
    
    print("\n===  Simple Expiry Check ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found to check.")
        return
    
    # Get today's date
    today = datetime.today().date()
    print(f"Today's date: {today}")
    
    # Convert expiry_date column to date format - break down the operation
    expiry_datetime = pd.to_datetime(ingredients['expiry_date'])
    ingredients['expiry_date'] = expiry_datetime.dt.date
    
    print(f"\n Checking {len(ingredients)} ingredients...")
    
    # Check each ingredient and show status
    safe_items = []
    expired_items = []
    
    for i, row in ingredients.iterrows():
        ingredient_name = row['name']
        expiry_date = row['expiry_date']
        quantity = row['quantity']
        unit = row['unit']
        
        # Compare today's date with expiry date
        if today > expiry_date:
            # Ingredient has expired
            expired_items.append(row)
            print(f" {ingredient_name} ({quantity} {unit}) - EXPIRED on {expiry_date}")
        else:
            # Ingredient is still safe - calculate days left
            safe_items.append(row)
            date_difference = expiry_date - today
            days_left = date_difference.days
            print(f" {ingredient_name} ({quantity} {unit}) - Safe (expires in {days_left} days)")
    
    # Show summary
    print(f"\n Summary:")
    print(f" Safe ingredients: {len(safe_items)}")
    print(f" Expired ingredients: {len(expired_items)}")
    
    # Ask user if they want to remove expired items
    if expired_items:
        print(f"\n Found {len(expired_items)} expired ingredient(s).")
        choice = input("Do you want to remove expired ingredients? (yes/no): ").strip().lower()
        
        if choice == 'yes':
            remove_expired_ingredients()
        else:
            print(" Expired ingredients kept in stock.")

def remove_expired_ingredients():
    # Remove expired ingredients from the database automatically
    # This function demonstrates DataFrame filtering and file operations
    # 
    # Uses syllabus concepts:
    # - Boolean indexing for filtering DataFrames
    # - Date comparison operations
    # - File writing with pandas to_csv()
    
    print("\n===  Removing Expired Ingredients ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found.")
        return
    
    # Get today's date
    today = datetime.today().date()
    
    # Convert expiry_date to date format
    ingredients['expiry_date'] = pd.to_datetime(ingredients['expiry_date']).dt.date
    
    # Find expired items using boolean indexing
    expired_items = ingredients[ingredients['expiry_date'] < today]
    
    # Keep only safe items (not expired)
    safe_ingredients = ingredients[ingredients['expiry_date'] >= today]
    
    # Show what will be removed
    if not expired_items.empty:
        print("\n Removing expired items:")
        for i, row in expired_items.iterrows():
            print(f"- {row['name']} {row['quantity']}{row['unit']} (Expired on {row['expiry_date']})")
        
        # Save updated ingredients (without expired items)
        save_ingredients(safe_ingredients)
        
        print(f"\n Removed {len(expired_items)} expired ingredient(s).")
        print(f" {len(safe_ingredients)} ingredients remaining in stock.")
    else:
        print("\n No expired items found today.")

def show_expiry_status():
    # Show detailed expiry status of all ingredients
    # This function demonstrates data analysis and formatting
    # 
    # Uses syllabus concepts:
    # - Pandas DataFrame operations
    # - Date calculations and comparison
    # - String formatting and conditional display
    
    print("\n===  Detailed Expiry Status ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found.")
        return
    
    # Get today's date
    today = datetime.today().date()
    
    # Convert expiry_date to date format
    ingredients['expiry_date'] = pd.to_datetime(ingredients['expiry_date']).dt.date
    
    # Calculate days until expiry for each ingredient (no .dt needed since we're working with date objects)
    ingredients['days_until_expiry'] = (ingredients['expiry_date'] - today).apply(lambda x: x.days)
    
    # Sort by days until expiry (most urgent first)
    ingredients_sorted = ingredients.sort_values('days_until_expiry')
    
    print(f"\n Expiry Status (sorted by urgency):")
    print("-" * 80)
    
    for i, row in ingredients_sorted.iterrows():
        name = row['name']
        quantity = row['quantity']
        unit = row['unit']
        expiry_date = row['expiry_date']
        days_left = row['days_until_expiry']
        
        # Determine status and color
        if days_left < 0:
            status = " EXPIRED"
            urgency = f"(expired {abs(days_left)} days ago)"
        elif days_left == 0:
            status = " EXPIRES TODAY"
            urgency = "(use immediately!)"
        elif days_left <= 2:
            status = " EXPIRES SOON"
            urgency = f"(expires in {days_left} day(s))"
        elif days_left <= 7:
            status = " GOOD"
            urgency = f"(expires in {days_left} days)"
        else:
            status = " FRESH"
            urgency = f"(expires in {days_left} days)"
        
        print(f"{name:<15} {quantity:>6} {unit:<8} {expiry_date} {status} {urgency}")
    
    print("-" * 80)
    
    # Show category summary
    expired_count = len(ingredients[ingredients['days_until_expiry'] < 0])
    expires_today = len(ingredients[ingredients['days_until_expiry'] == 0])
    expires_soon = len(ingredients[(ingredients['days_until_expiry'] > 0) & (ingredients['days_until_expiry'] <= 2)])
    
    print(f"\n Summary:")
    print(f" Expired: {expired_count}")
    print(f" Expires today: {expires_today}")
    print(f" Expires soon (1-2 days): {expires_soon}")
    print(f" Total ingredients: {len(ingredients)}")

def check_specific_ingredient():
    # Check expiry status of a specific ingredient
    # This function demonstrates user input and data filtering
    # 
    # Uses syllabus concepts:
    # - User input with input() function
    # - DataFrame filtering with boolean indexing
    # - String operations and conditional statements
    
    print("\n===  Check Specific Ingredient ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found.")
        return
    
    # Show available ingredients
    print("\nAvailable ingredients:")
    for name in ingredients['name'].unique():
        print(f"- {name}")
    
    # Get user input
    ingredient_name = input("\nEnter ingredient name to check: ").strip().title()
    
    # Find the ingredient using boolean indexing
    ingredient_data = ingredients[ingredients['name'] == ingredient_name]
    
    if len(ingredient_data) == 0:
        print(f" Ingredient '{ingredient_name}' not found in stock.")
        return
    
    # Get today's date
    today = datetime.today().date()
    
    # Process the ingredient data
    for i, row in ingredient_data.iterrows():
        expiry_date = pd.to_datetime(row['expiry_date']).date()
        quantity = row['quantity']
        unit = row['unit']
        storage = row['storage_type']
        
        # Calculate days until expiry
        days_left = (expiry_date - today).days
        
        print(f"\n Ingredient Details:")
        print(f"Name: {ingredient_name}")
        print(f"Quantity: {quantity} {unit}")
        print(f"Storage: {storage}")
        print(f"Expiry Date: {expiry_date}")
        
        # Show status
        if days_left < 0:
            print(f"Status:  EXPIRED ({abs(days_left)} days ago)")
            print(" This ingredient should be discarded!")
        elif days_left == 0:
            print(f"Status:  EXPIRES TODAY")
            print(" Use this ingredient immediately!")
        elif days_left <= 2:
            print(f"Status:  EXPIRES SOON ({days_left} day(s))")
            print(" Plan to use this ingredient in the next meal!")
        else:
            print(f"Status:  FRESH ({days_left} days remaining)")
            print(" This ingredient is safe to use!")

def expiry_check_menu():
    # Main menu for simple expiry checking features
    # This function demonstrates menu-driven programming
    # 
    # Uses syllabus concepts:
    # - while loop for menu repetition
    # - if-elif-else for menu choices
    # - Function calls and program flow control
    
    while True:
        print("\n" + "="*50)
        print(" SIMPLE EXPIRY CHECK")
        print("="*50)
        print("1. Check All Ingredients")
        print("2. Remove Expired Ingredients")
        print("3. Show Detailed Expiry Status")
        print("4. Check Specific Ingredient")
        print("5. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-5): ").strip()
        
        if choice == "1":
            check_expiry_simple()
        elif choice == "2":
            remove_expired_ingredients()
        elif choice == "3":
            show_expiry_status()
        elif choice == "4":
            check_specific_ingredient()
        elif choice == "5":
            print(" Returning to main menu...")
            break
        else:
            print(" Invalid choice! Please enter a number between 1-5.")

# Test function for development
if __name__ == "__main__":
    # This runs only when the file is executed directly
    print("Testing Simple Expiry Check Module...")
    expiry_check_menu()
