# Feature 3: Waste Management Module
#
# This module handles food waste tracking and management:
# - Record wasted ingredients
# - View waste history
# - Calculate waste cost
# - Suggest waste reduction tips
#
# Uses concepts from syllabus:
# - Pandas for CSV operations
# - Datetime for date handling
# - Functions and input/output
# - String operations and validation
# - Mathematical operations for cost calculation

# Import required libraries (all from syllabus)
import pandas as pd  # For CSV operations and data manipulation
from datetime import datetime  # For date handling
import os  # For file path operations

def get_data_file_path(filename):
    # Get the correct path to data files
    # This function handles different execution contexts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_path = os.path.join(parent_dir, "data", filename)

    # If data directory doesn't exist, create it
    data_dir = os.path.dirname(data_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_path

def load_waste_data():
    # Load waste data from CSV file
    # This function demonstrates file handling and exception handling
    #
    # Returns: pandas DataFrame with waste data
    #
    # Uses syllabus concepts:
    # - Pandas read_csv() function
    # - Exception handling with try-except
    # - DataFrame creation with specific columns
    try:
        # Get correct file path
        waste_file = get_data_file_path("waste.csv")

        # Read waste CSV file using pandas
        waste_df = pd.read_csv(waste_file)
        return waste_df
    except FileNotFoundError:
        # If file doesn't exist, create empty DataFrame with required columns
        print("WARNING: Waste file not found. Creating new waste database...")
        columns = ['id', 'name', 'quantity', 'unit', 'reason', 'date', 'cost']
        waste_df = pd.DataFrame(columns=columns)

        # Save the empty DataFrame to create the file
        waste_file = get_data_file_path("waste.csv")
        waste_df.to_csv(waste_file, index=False)
        print(f"SUCCESS: Created new waste database at: {waste_file}")

        return waste_df

def save_waste_data(df):
    # Save waste DataFrame to CSV file
    # This function demonstrates file writing operations
    #
    # Args: df (pandas DataFrame) - waste data to save
    #
    # Uses syllabus concepts:
    # - Pandas to_csv() method
    # - File writing without index
    try:
        # Get correct file path
        waste_file = get_data_file_path("waste.csv")

        # Save to CSV without index column
        df.to_csv(waste_file, index=False)
    except Exception as e:
        print(f"ERROR: Error saving waste data: {e}")
        print("TIP: Please check file permissions and try again.")

def add_waste_entry():
    # Add a new waste entry to the database
    # This function demonstrates user input validation and data processing
    #
    # Uses syllabus concepts:
    # - input() function for user interaction
    # - String methods: strip(), title(), lower()
    # - Data type conversion with float() and int()
    # - Exception handling for input validation
    # - Datetime operations
    # - Dictionary creation and DataFrame operations
    print("\n=== Add Waste Entry ===")
    
    # Load current waste data
    waste_df = load_waste_data()
    
    # Get ingredient name from user - break down the chained operations for clarity
    user_input = input("Enter ingredient name that was wasted: ")  # Get input from user
    clean_input = user_input.strip()  # Remove extra spaces from beginning and end
    name = clean_input.title()  # Convert to Title Case (First Letter Capitalized)

    # Get quantity with validation - keep asking until we get a valid number
    quantity = 0  # Initialize quantity variable
    while True:  # Keep looping until we get valid input
        try:  # Try to convert user input to a number
            user_quantity = input("Enter quantity wasted: ")  # Get quantity from user
            quantity = float(user_quantity)  # Convert string to decimal number

            # Check if quantity is positive (greater than 0)
            if quantity <= 0:
                print("WARNING: Quantity must be positive. Please try again.")
            else:
                break  # Exit the loop if quantity is valid (positive number)

        except ValueError:
            # This runs if user enters something that can't be converted to a number
            print("WARNING: Please enter a valid number for quantity.")
    
    # Get unit with validation - replace complex string operations with simple loops
    valid_units = ['g', 'kg', 'ml', 'l', 'pieces', 'slices']

    # Create unit options string using simple loop instead of join()
    unit_options = ""
    for unit_option in valid_units:
        unit_options = unit_options + unit_option + "/"
    unit_options = unit_options[:-1]  # Remove last slash

    unit = ""
    while True:
        user_unit = input(f"Enter unit ({unit_options}): ")
        clean_unit = user_unit.strip()
        unit = clean_unit.lower()

        # Check if unit is valid using simple loop instead of 'in' operator
        unit_found = False
        for valid_unit in valid_units:
            if unit == valid_unit:
                unit_found = True
                break

        if unit_found:
            break
        else:
            # Create error message using simple loop
            valid_units_text = ""
            for valid_unit in valid_units:
                valid_units_text = valid_units_text + valid_unit + ", "
            valid_units_text = valid_units_text[:-2]  # Remove last comma and space
            print(f"WARNING: Please enter a valid unit: {valid_units_text}")
    
    # Get waste reason with validation - use simple loops instead of join()
    valid_reasons = ['expired', 'spoiled', 'leftover', 'overcooked', 'burnt']

    # Create reasons text using simple loop
    reasons_text = ""
    for reason_option in valid_reasons:
        reasons_text = reasons_text + reason_option + ", "
    reasons_text = reasons_text[:-2]  # Remove last comma and space
    print(f"Waste reasons: {reasons_text}")

    reason = ""
    while True:
        user_reason = input("Enter reason for waste: ")
        clean_reason = user_reason.strip()
        reason_lower = clean_reason.lower()

        # Check if reason is valid using simple loop
        reason_found = False
        for valid_reason in valid_reasons:
            if reason_lower == valid_reason:
                reason_found = True
                reason = reason_lower.title()  # Convert to title case
                break

        if reason_found:
            break
        else:
            print(f"WARNING: Please enter a valid reason: {reasons_text}")
    
    # Get cost with validation
    cost = 0
    while True:
        try:
            user_cost = input("Enter estimated cost of wasted item: ")
            cost = float(user_cost)
            if cost < 0:
                print("WARNING: Cost cannot be negative. Please try again.")
            else:
                break  # Exit loop if cost is valid
        except ValueError:
            print("WARNING: Please enter a valid number for cost.")

    # Generate new ID - break down the logic
    waste_count = len(waste_df)
    if waste_count == 0:
        new_id = 1
    else:
        max_id = waste_df['id'].max()
        new_id = max_id + 1

    # Get current date - break down the chained operations
    current_date = datetime.today()
    today = current_date.strftime("%Y-%m-%d")

    # Create new waste entry dictionary - use separate lines for clarity
    new_waste = {}
    new_waste['id'] = new_id
    new_waste['name'] = name
    new_waste['quantity'] = quantity
    new_waste['unit'] = unit
    new_waste['reason'] = reason
    new_waste['date'] = today
    new_waste['cost'] = cost

    # Add to DataFrame - create new row first, then add
    new_row_df = pd.DataFrame([new_waste])
    waste_df = pd.concat([waste_df, new_row_df], ignore_index=True)

    # Save to file
    save_waste_data(waste_df)

    print(f"SUCCESS: Waste entry for '{name}' added successfully!")
    cost_formatted = f"₹{cost:.2f}"
    print(f"COST: Estimated loss: {cost_formatted}")

def view_waste_history():
    # Display waste history with various viewing options
    # This function demonstrates DataFrame operations and data analysis
    #
    # Uses syllabus concepts:
    # - Pandas DataFrame operations
    # - sort_values() method for sorting
    # - groupby() for data aggregation
    # - sum() function for calculations
    # - String formatting and conditional statements
    print("\n===  Waste History ===")
    
    # Load waste data
    waste_df = load_waste_data()
    
    if len(waste_df) == 0:
        print("INFO: No waste entries found.")
        return
    
    # Display viewing options
    print("\nView Options:")
    print("1. All waste entries")
    print("2. Sort by date (newest first)")
    print("3. Filter by reason")
    print("4. Summary by ingredient")
    print("5. Monthly waste summary")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        # Show all waste entries
        display_waste_table(waste_df)
    
    elif choice == "2":
        # Sort by date (newest first)
        waste_sorted = waste_df.sort_values(by='date', ascending=False)
        print("\n Waste entries sorted by date (newest first):")
        display_waste_table(waste_sorted)
    
    elif choice == "3":
        # Filter by reason
        print(f"\nAvailable reasons: {', '.join(waste_df['reason'].unique())}")
        reason = input("Enter reason to filter by: ").strip().title()
        filtered = waste_df[waste_df['reason'] == reason]
        if len(filtered) == 0:
            print(f"INFO: No waste entries found for reason '{reason}'.")
        else:
            print(f"\n Waste entries for reason '{reason}':")
            display_waste_table(filtered)
    
    elif choice == "4":
        # Summary by ingredient using groupby
        print("\n Waste Summary by Ingredient:")
        summary = waste_df.groupby('name').agg({
            'quantity': 'sum',
            'cost': 'sum'
        }).round(2)
        print(summary.to_string())
        
        # Calculate total waste cost
        total_cost = waste_df['cost'].sum()
        print(f"\nCOST: Total waste cost: ₹{total_cost:.2f}")
    
    elif choice == "5":
        # Monthly summary (simplified - just by month-year)
        print("\n Monthly Waste Summary:")
        # Convert date column to datetime for better processing
        waste_df['date'] = pd.to_datetime(waste_df['date'])
        waste_df['month_year'] = waste_df['date'].dt.strftime('%Y-%m')
        
        monthly_summary = waste_df.groupby('month_year').agg({
            'cost': 'sum',
            'id': 'count'  # Count number of entries
        }).round(2)
        monthly_summary.columns = ['Total_Cost', 'Number_of_Entries']
        print(monthly_summary.to_string())
    
    else:
        print("WARNING: Invalid choice. Showing all waste entries:")
        display_waste_table(waste_df)

def display_waste_table(df):
    # Display waste DataFrame in a formatted table
    # This function demonstrates DataFrame display operations
    #
    # Args: df (pandas DataFrame) - waste data to display
    #
    # Uses syllabus concepts:
    # - Pandas to_string() method
    # - len() function for counting
    # - Conditional statements
    if len(df) == 0:
        print("INFO: No waste entries to display.")
        return
    
    # Use pandas to_string for clean table display
    print(df.to_string(index=False))
    print(f"\n Total entries: {len(df)}")
    
    # Calculate and show total cost
    total_cost = df['cost'].sum()
    print(f"COST: Total waste cost: ₹{total_cost:.2f}")

def waste_reduction_tips():
    # Provide waste reduction tips based on waste history
    # This function demonstrates data analysis and conditional logic
    #
    # Uses syllabus concepts:
    # - DataFrame analysis operations
    # - Conditional statements (if-elif-else)
    # - String operations and print formatting
    print("\n=== TIP: Waste Reduction Tips ===")
    
    # Load waste data
    waste_df = load_waste_data()
    
    if len(waste_df) == 0:
        print("INFO: No waste data available for analysis.")
        return
    
    # Analyze most common waste reasons
    reason_counts = waste_df['reason'].value_counts()
    most_common_reason = reason_counts.index[0]
    
    print(f" Analysis of your waste patterns:")
    print(f"Most common waste reason: {most_common_reason}")
    print(f"Occurrences: {reason_counts.iloc[0]}")
    
    # Provide specific tips based on most common reason
    if most_common_reason.lower() == 'expired':
        print("\nTIP: Tips to reduce expiry waste:")
        print("- Check expiry dates regularly")
        print("- Use FIFO (First In, First Out) method")
        print("- Plan meals based on expiry dates")
        print("- Store ingredients properly")
    
    elif most_common_reason.lower() == 'spoiled':
        print("\nTIP: Tips to reduce spoilage:")
        print("- Improve storage conditions")
        print("- Check temperature settings")
        print("- Use proper containers")
        print("- Consume perishables quickly")
    
    elif most_common_reason.lower() == 'leftover':
        print("\nTIP: Tips to reduce leftovers:")
        print("- Plan portion sizes better")
        print("- Cook smaller quantities")
        print("- Store leftovers properly")
        print("- Create new recipes from leftovers")
    
    elif most_common_reason.lower() == 'overcooked':
        print("\nTIP: Tips to reduce overcooking:")
        print("- Use timers while cooking")
        print("- Monitor cooking temperature")
        print("- Practice cooking techniques")
        print("- Follow recipes carefully")
    
    else:
        print("\nTIP: General waste reduction tips:")
        print("- Plan your meals in advance")
        print("- Buy only what you need")
        print("- Store food properly")
        print("- Use ingredients before they expire")
    
    # Show total waste cost impact
    total_cost = waste_df['cost'].sum()
    print(f"\nCOST: Total money lost to waste: ₹{total_cost:.2f}")
    print("TIP: Reducing waste can save you money!")

def delete_waste_entry():
    # Delete a waste entry from the database
    # This function demonstrates DataFrame filtering and user confirmation
    #
    # Uses syllabus concepts:
    # - DataFrame filtering with boolean indexing
    # - User input validation
    # - Conditional statements for confirmation
    print("\n===  Delete Waste Entry ===")
    
    # Load waste data
    waste_df = load_waste_data()
    
    if len(waste_df) == 0:
        print("INFO: No waste entries found to delete.")
        return
    
    # Show current waste entries for reference
    print("\nCurrent waste entries:")
    print(waste_df[['id', 'name', 'quantity', 'unit', 'reason', 'date']].to_string(index=False))
    
    # Get waste entry ID to delete
    while True:
        try:
            waste_id = int(input("\nEnter waste entry ID to delete: "))
            # Check if ID exists using membership operator
            if waste_id in waste_df['id'].values:
                break
            else:
                print("WARNING: Waste entry ID not found. Please try again.")
        except ValueError:
            print("WARNING: Please enter a valid number for ID.")
    
    # Get waste entry info for confirmation
    waste_to_delete = waste_df[waste_df['id'] == waste_id].iloc[0]
    
    # Confirm deletion
    print(f"\nAre you sure you want to delete this waste entry?")
    print(f"ID: {waste_to_delete['id']}")
    print(f"Item: {waste_to_delete['name']}")
    print(f"Quantity: {waste_to_delete['quantity']} {waste_to_delete['unit']}")
    print(f"Reason: {waste_to_delete['reason']}")
    print(f"Date: {waste_to_delete['date']}")
    
    confirmation = input("\nType 'yes' to confirm deletion: ").strip().lower()
    
    if confirmation == 'yes':
        # Remove the waste entry (keep all rows except the one with matching ID)
        waste_df = waste_df[waste_df['id'] != waste_id]
        
        # Save changes
        save_waste_data(waste_df)
        
        print(f"SUCCESS: Waste entry for {waste_to_delete['name']} deleted successfully.")
    else:
        print("ERROR: Deletion cancelled.")

def waste_management_menu():
    # Main menu for waste management features
    # This function demonstrates menu-driven programming
    #
    # Uses syllabus concepts:
    # - while loop for menu repetition
    # - if-elif-else for menu choices
    # - Function calls and program flow control
    while True:
        print("\n" + "="*50)
        print(" WASTE MANAGEMENT")
        print("="*50)
        print("1. Add Waste Entry")
        print("2. View Waste History")
        print("3. Waste Reduction Tips")
        print("4. Delete Waste Entry")
        print("5. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_waste_entry()
        elif choice == "2":
            view_waste_history()
        elif choice == "3":
            waste_reduction_tips()
        elif choice == "4":
            delete_waste_entry()
        elif choice == "5":
            print(" Returning to main menu...")
            break
        else:
            print("WARNING: Invalid choice! Please enter a number between 1-5.")

# Test function for development
if __name__ == "__main__":
    # This runs only when the file is executed directly
    print("Testing Waste Management Module...")
    waste_management_menu()
