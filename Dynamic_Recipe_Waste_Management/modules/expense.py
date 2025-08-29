# Feature 7: Expense Tracker
#
# This module handles expense tracking for ingredients:
# - Add expense records when buying ingredients
# - View total expenses
# - View ingredient-wise expenses
# - Simple expense management
#
# Uses concepts from syllabus:
# - Pandas for CSV operations
# - Mathematical operations for cost calculation
# - Functions and input/output
# - Data aggregation with groupby()

# Import required libraries (all from syllabus)
import pandas as pd  # For CSV operations and data manipulation
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

def load_expenses():
    # Load expenses from CSV file
    # Returns: pandas DataFrame with expense data
    try:
        # Read expenses CSV file using correct path
        expenses_file = get_data_file_path("expenses.csv")
        expenses_df = pd.read_csv(expenses_file)
        return expenses_df
    except FileNotFoundError:
        # If file doesn't exist, create empty DataFrame with required columns
        print(" Expenses file not found. Creating new expense database...")
        columns = ['id', 'name', 'cost']
        expenses_df = pd.DataFrame(columns=columns)

        # Save the empty DataFrame to create the file
        expenses_file = get_data_file_path("expenses.csv")
        expenses_df.to_csv(expenses_file, index=False)
        print(f" Created new expenses database at: {expenses_file}")

        return expenses_df

def save_expenses(df):
    # Save expenses DataFrame to CSV file
    # Args: df (pandas DataFrame) - expense data to save
    try:
        expenses_file = get_data_file_path("expenses.csv")
        df.to_csv(expenses_file, index=False)
    except Exception as e:
        print(f" Error saving expenses: {e}")

def add_expense():
    # Add a new expense entry to the database
    # This function demonstrates user input and data processing
    # 
    # Uses syllabus concepts:
    # - input() function for user interaction
    # - String methods: strip(), title()
    # - Data type conversion with float()
    # - Exception handling for input validation
    # - Dictionary creation and DataFrame operations
    
    print("\n===  Add Expense ===")
    
    # Load current expenses
    expenses = load_expenses()
    
    # Get ingredient name from user - break down chained operations
    user_input = input("Enter ingredient name: ")
    clean_input = user_input.strip()
    name = clean_input.title()

    # Get cost with validation
    cost = 0
    while True:
        try:
            user_cost = input("Enter cost: ")
            cost = float(user_cost)
            if cost < 0:
                print(" Cost cannot be negative. Please try again.")
            else:
                break  # Exit loop if cost is valid
        except ValueError:
            print(" Please enter a valid number for cost.")

    # Generate new ID - break down the logic
    expenses_count = len(expenses)
    if expenses_count == 0:
        new_id = 1
    else:
        max_id = expenses['id'].max()
        new_id = max_id + 1

    # Create new expense dictionary - use separate lines for clarity
    new_expense = {}
    new_expense['id'] = new_id
    new_expense['name'] = name
    new_expense['cost'] = cost

    # Add to DataFrame - create new row first, then add
    new_row_df = pd.DataFrame([new_expense])
    expenses = pd.concat([expenses, new_row_df], ignore_index=True)
    
    # Save to file
    save_expenses(expenses)
    
    print(f" Expense for '{name}' recorded successfully!")
    print(f" Cost: ₹{cost:.2f}")

def view_total_expenses():
    # View total expenses across all ingredients
    # This function demonstrates data aggregation and mathematical operations
    # 
    # Uses syllabus concepts:
    # - Pandas sum() function for aggregation
    # - Mathematical operations and formatting
    # - Conditional statements for data validation
    
    print("\n===  Total Expenses ===")
    
    # Load expenses
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print(" No expense records found.")
        return
    
    # Calculate total expenses using sum() function
    total_cost = expenses['cost'].sum()
    
    # Show total
    print(f"\n Total Expenses: ₹{total_cost:.2f}")
    print(f" Number of expense entries: {len(expenses)}")

    # Calculate average cost per ingredient
    if len(expenses) > 0:
        average_cost = total_cost / len(expenses)
        print(f" Average cost per entry: ₹{average_cost:.2f}")

def view_ingredient_wise_expenses():
    # View expenses grouped by ingredient name
    # This function demonstrates data grouping and aggregation
    # 
    # Uses syllabus concepts:
    # - Pandas groupby() function for data aggregation
    # - sum() function for calculating totals
    # - DataFrame operations and display
    
    print("\n===  Ingredient-wise Expenses ===")
    
    # Load expenses
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print(" No expense records found.")
        return
    
    # Group by ingredient name and sum the costs - break down operations
    grouped_expenses = expenses.groupby('name')
    ingredient_wise = grouped_expenses['cost'].sum()

    # Sort by cost (highest first)
    ingredient_wise_sorted = ingredient_wise.sort_values(ascending=False)
    
    print(f"\n Expenses by Ingredient:")
    print("-" * 40)
    
    # Display each ingredient and its total cost
    for ingredient, total_cost in ingredient_wise_sorted.items():
        print(f"{ingredient:<20} ₹{total_cost:>8.2f}")

    print("-" * 40)

    # Show summary statistics
    total_cost = ingredient_wise.sum()
    most_expensive = ingredient_wise_sorted.index[0]
    highest_cost = ingredient_wise_sorted.iloc[0]

    print(f" Total: ₹{total_cost:.2f}")
    print(f" Most expensive: {most_expensive} (₹{highest_cost:.2f})")
    print(f" Number of different ingredients: {len(ingredient_wise)}")

def view_all_expenses():
    # View all expense records in detail
    # This function demonstrates DataFrame display and formatting
    # 
    # Uses syllabus concepts:
    # - Pandas DataFrame display operations
    # - to_string() method for clean formatting
    # - len() function for counting records
    
    print("\n===  All Expense Records ===")
    
    # Load expenses
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print(" No expense records found.")
        return
    
    # Display all expenses in table format
    print("\nAll expense records:")
    print(expenses.to_string(index=False))
    
    # Show summary
    total_cost = expenses['cost'].sum()
    print(f"\n Summary:")
    print(f"Total records: {len(expenses)}")
    print(f"Total expenses: ₹{total_cost:.2f}")

def delete_expense():
    # Delete an expense record from the database
    # This function demonstrates DataFrame filtering and user confirmation
    # 
    # Uses syllabus concepts:
    # - DataFrame filtering with boolean indexing
    # - User input validation
    # - Conditional statements for confirmation
    
    print("\n===  Delete Expense Record ===")
    
    # Load expenses
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print(" No expense records found to delete.")
        return
    
    # Show current expense records for reference
    print("\nCurrent expense records:")
    print(expenses[['id', 'name', 'cost']].to_string(index=False))
    
    # Get expense ID to delete
    while True:
        try:
            expense_id = int(input("\nEnter expense ID to delete: "))
            # Check if ID exists using membership operator
            if expense_id in expenses['id'].values:
                break
            else:
                print(" Expense ID not found. Please try again.")
        except ValueError:
            print(" Please enter a valid number for ID.")
    
    # Get expense info for confirmation
    expense_to_delete = expenses[expenses['id'] == expense_id].iloc[0]
    
    # Confirm deletion
    print(f"\nAre you sure you want to delete this expense record?")
    print(f"ID: {expense_to_delete['id']}")
    print(f"Ingredient: {expense_to_delete['name']}")
    print(f"Cost: ₹{expense_to_delete['cost']:.2f}")
    
    confirmation = input("\nType 'yes' to confirm deletion: ").strip().lower()
    
    if confirmation == 'yes':
        # Remove the expense record (keep all rows except the one with matching ID)
        expenses = expenses[expenses['id'] != expense_id]
        
        # Save changes
        save_expenses(expenses)
        
        print(f" Expense record for {expense_to_delete['name']} deleted successfully.")
    else:
        print(" Deletion cancelled.")

def expense_summary():
    # Show a comprehensive expense summary
    # This function demonstrates data analysis and statistical operations
    # 
    # Uses syllabus concepts:
    # - Multiple pandas aggregation functions
    # - Mathematical operations and calculations
    # - Conditional statements and data analysis
    
    print("\n===  Expense Summary ===")
    
    # Load expenses
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print(" No expense records found.")
        return
    
    # Calculate various statistics
    total_cost = expenses['cost'].sum()
    average_cost = expenses['cost'].mean()
    min_cost = expenses['cost'].min()
    max_cost = expenses['cost'].max()
    num_records = len(expenses)
    num_ingredients = expenses['name'].nunique()
    
    print(f"\n Financial Summary:")
    print(f" Total Expenses: ₹{total_cost:.2f}")
    print(f" Average Cost per Entry: ₹{average_cost:.2f}")
    print(f" Minimum Cost: ₹{min_cost:.2f}")
    print(f" Maximum Cost: ₹{max_cost:.2f}")
    print(f" Total Records: {num_records}")
    print(f" Different Ingredients: {num_ingredients}")

    # Find most and least expensive ingredients
    ingredient_totals = expenses.groupby('name')['cost'].sum().sort_values(ascending=False)

    if len(ingredient_totals) > 0:
        most_expensive = ingredient_totals.index[0]
        most_expensive_cost = ingredient_totals.iloc[0]
        least_expensive = ingredient_totals.index[-1]
        least_expensive_cost = ingredient_totals.iloc[-1]

        print(f"\n Top Spender: {most_expensive} (₹{most_expensive_cost:.2f})")
        print(f" Least Expensive: {least_expensive} (₹{least_expensive_cost:.2f})")

def expense_tracker_menu():
    # Main menu for expense tracking features
    # This function demonstrates menu-driven programming
    # 
    # Uses syllabus concepts:
    # - while loop for menu repetition
    # - if-elif-else for menu choices
    # - Function calls and program flow control
    
    while True:
        print("\n" + "="*50)
        print(" EXPENSE TRACKER")
        print("="*50)
        print("1. Add Expense")
        print("2. View Total Expenses")
        print("3. View Ingredient-wise Expenses")
        print("4. View All Expense Records")
        print("5. Delete Expense Record")
        print("6. Expense Summary")
        print("7. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_total_expenses()
        elif choice == "3":
            view_ingredient_wise_expenses()
        elif choice == "4":
            view_all_expenses()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            expense_summary()
        elif choice == "7":
            print(" Returning to main menu...")
            break
        else:
            print(" Invalid choice! Please enter a number between 1-7.")

# Test function for development
if __name__ == "__main__":
    # This runs only when the file is executed directly
    print("Testing Expense Tracker Module...")
    expense_tracker_menu()
