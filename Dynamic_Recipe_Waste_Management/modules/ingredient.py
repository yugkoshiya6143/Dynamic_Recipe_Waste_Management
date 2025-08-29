# Feature 1: Ingredient Management Module
# This is the first major feature of our kitchen management system
#
# This module handles all ingredient-related operations:
# - Add new ingredients to our inventory
# - View current stock of ingredients
# - Update ingredient quantities when we use them
# - Remove ingredients from our inventory
#
# Uses concepts from syllabus:
# - Pandas for CSV operations (reading and writing data files)
# - Datetime for date handling (tracking when ingredients were added)
# - Dictionaries for data storage (organizing ingredient information)
# - Functions and input/output (getting information from user)
# - String operations and validation (cleaning and checking user input)

# Import required libraries - these give us extra functionality
import pandas as pd        # For working with CSV files and data tables
from datetime import datetime  # For working with dates and times
import os                 # For working with file paths and directories

def get_data_file_path(filename):
    # Get the correct path to data files
    # This function helps us find the right location for our data files
    # no matter where the program is run from

    # Get the absolute path of this current file
    current_file_path = __file__  # __file__ is the path to this Python file
    absolute_current_path = os.path.abspath(current_file_path)  # Make it absolute
    current_dir = os.path.dirname(absolute_current_path)  # Get just the directory part

    # Go up one level to get the parent directory (project root)
    parent_dir = os.path.dirname(current_dir)

    # Create the path to the data file
    data_path = os.path.join(parent_dir, "data", filename)  # Join paths together

    # If data directory doesn't exist, create it
    data_dir = os.path.dirname(data_path)  # Get the directory part of the data path
    directory_exists = os.path.exists(data_dir)  # Check if directory exists
    if not directory_exists:  # If directory doesn't exist
        os.makedirs(data_dir)  # Create the directory

    return data_path  # Return the complete path to the data file

def load_ingredients():
    # Load ingredients from CSV file
    # This function reads our ingredient data from a CSV file
    # Returns: pandas DataFrame (a table of ingredient data)

    # Use try-except to handle errors gracefully
    try:
        # Get the correct file path for ingredients.csv
        ingredients_file = get_data_file_path("ingredients.csv")

        # Read CSV file using pandas - this creates a DataFrame (data table)
        df = pd.read_csv(ingredients_file)
        return df  # Return the DataFrame to whoever called this function

    except FileNotFoundError:
        # This block runs if the ingredients.csv file doesn't exist yet

        # Tell the user we're creating a new database
        print(" Ingredients file not found. Creating new database...")

        # Define the column names for our ingredients table
        columns = ['id', 'name', 'quantity', 'unit', 'expiry_date', 'storage_type', 'date_added', 'cost']

        # Create an empty DataFrame with these columns
        df = pd.DataFrame(columns=columns)

        # Save the empty DataFrame to create the file
        ingredients_file = get_data_file_path("ingredients.csv")  # Get file path again
        df.to_csv(ingredients_file, index=False)  # Save to CSV without row numbers

        # Tell the user where we created the file
        success_message = f" Created new ingredients database at: {ingredients_file}"
        print(success_message)

        return df  # Return the empty DataFrame

def save_ingredients(df):
    # Save ingredients DataFrame to CSV file
    # Args: df (pandas DataFrame) - ingredients data
    try:
        # Get correct file path
        ingredients_file = get_data_file_path("ingredients.csv")

        # Save to CSV without index
        df.to_csv(ingredients_file, index=False)
    except Exception as e:
        print(f" Error saving ingredients data: {e}")
        print(" Please check file permissions and try again.")

def add_ingredient():
    # Add a new ingredient to the database
    #
    # BEGINNER EXPLANATION:
    # This function asks the user for ingredient information (name, quantity, unit,
    # expiry date, storage type, and cost) and saves it to our CSV file.
    # It includes validation to make sure the user enters correct information.
    #
    # Uses: input(), dictionaries, datetime, pandas operations
    print("\n===  Add New Ingredient ===")

    # Load current ingredients from our CSV file
    ingredients = load_ingredients()
    
    # Step 1: Get ingredient name from user
    # We break down the operations to make it easier to understand
    user_input = input("Enter ingredient name: ")  # Get input from user
    clean_input = user_input.strip()  # Remove extra spaces
    name = clean_input.title()  # Make first letter of each word uppercase

    # Step 2: Get quantity with validation
    # We use a while loop to keep asking until we get a valid number
    quantity = 0  # Initialize quantity variable
    while True:  # Keep looping until we get valid input
        try:
            user_quantity = input("Enter quantity: ")  # Ask for quantity
            quantity = float(user_quantity)  # Try to convert to number
            if quantity <= 0:  # Check if quantity is positive
                print(" Quantity must be positive. Please try again.")
            else:
                break  # Exit loop if quantity is valid
        except ValueError:  # This runs if conversion to float fails
            print(" Please enter a valid number for quantity.")

    # Get unit with validation - use simple loops instead of join()
    valid_units = ['g', 'kg', 'ml', 'l', 'pieces', 'slices']

    # Create unit options string using simple loop
    unit_options = ""
    for unit_option in valid_units:
        unit_options = unit_options + unit_option + "/"
    unit_options = unit_options[:-1]  # Remove last slash

    unit = ""
    while True:
        user_unit = input(f"Enter unit ({unit_options}): ")
        clean_unit = user_unit.strip()
        unit = clean_unit.lower()

        # Check if unit is valid using simple loop
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
            print(f" Please enter a valid unit: {valid_units_text}")
    
    # Get expiry date with validation
    expiry_date = ""
    while True:
        user_date = input("Enter expiry date (YYYY-MM-DD): ")
        expiry_date = user_date.strip()
        try:
            # Validate date format
            datetime.strptime(expiry_date, "%Y-%m-%d")
            break  # Exit loop if date is valid
        except ValueError:
            print(" Please enter date in YYYY-MM-DD format (e.g., 2025-08-25)")

    # Get storage type with validation - use simple loops
    valid_storage = ['fridge', 'pantry', 'freezer']

    # Create storage options string using simple loop
    storage_options = ""
    for storage_option in valid_storage:
        storage_options = storage_options + storage_option + "/"
    storage_options = storage_options[:-1]  # Remove last slash

    storage_type = ""
    while True:
        user_storage = input(f"Enter storage type ({storage_options}): ")
        clean_storage = user_storage.strip()
        storage_type = clean_storage.lower()

        # Check if storage type is valid using simple loop
        storage_found = False
        for valid_type in valid_storage:
            if storage_type == valid_type:
                storage_found = True
                break

        if storage_found:
            break
        else:
            # Create error message using simple loop
            valid_storage_text = ""
            for valid_type in valid_storage:
                valid_storage_text = valid_storage_text + valid_type + ", "
            valid_storage_text = valid_storage_text[:-2]  # Remove last comma and space
            print(f" Please enter a valid storage type: {valid_storage_text}")
    
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
    ingredients_count = len(ingredients)
    if ingredients_count == 0:
        new_id = 1
    else:
        max_id = ingredients['id'].max()
        new_id = max_id + 1

    # Get current date - break down chained operations
    current_date = datetime.today()
    today = current_date.strftime("%Y-%m-%d")

    # Create new ingredient dictionary - use separate lines for clarity
    new_ingredient = {}
    new_ingredient['id'] = new_id
    new_ingredient['name'] = name
    new_ingredient['quantity'] = quantity
    new_ingredient['unit'] = unit
    new_ingredient['expiry_date'] = expiry_date
    new_ingredient['storage_type'] = storage_type
    new_ingredient['date_added'] = today
    new_ingredient['cost'] = cost

    # Add to DataFrame - create new row first, then add
    new_row_df = pd.DataFrame([new_ingredient])
    ingredients = pd.concat([ingredients, new_row_df], ignore_index=True)
    
    # Save to file
    save_ingredients(ingredients)
    
    print(f" Ingredient '{name}' added successfully!")

def view_ingredients():
    # Display all ingredients in a formatted table
    # Uses: pandas operations, string formatting
    print("\n===  Current Ingredient Stock ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found in stock.")
        return
    
    # Display options for viewing
    print("\nView Options:")
    print("1. All ingredients")
    print("2. Sort by expiry date")
    print("3. Filter by storage type")
    print("4. Search by name")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        # Show all ingredients
        display_ingredients_table(ingredients)
    
    elif choice == "2":
        # Sort by expiry date
        ingredients_sorted = ingredients.sort_values(by='expiry_date')
        print("\n Ingredients sorted by expiry date:")
        display_ingredients_table(ingredients_sorted)
    
    elif choice == "3":
        # Filter by storage type
        storage_type = input("Enter storage type (fridge/pantry/freezer): ").strip().lower()
        filtered = ingredients[ingredients['storage_type'] == storage_type]
        if len(filtered) == 0:
            print(f" No ingredients found in {storage_type}.")
        else:
            print(f"\n🏠 Ingredients in {storage_type}:")
            display_ingredients_table(filtered)
    
    elif choice == "4":
        # Search by name
        search_name = input("Enter ingredient name to search: ").strip().lower()
        # Use string contains for partial matching
        filtered = ingredients[ingredients['name'].str.lower().str.contains(search_name)]
        if len(filtered) == 0:
            print(f" No ingredients found matching '{search_name}'.")
        else:
            print(f"\n Search results for '{search_name}':")
            display_ingredients_table(filtered)
    
    else:
        print(" Invalid choice. Showing all ingredients:")
        display_ingredients_table(ingredients)

def display_ingredients_table(df):
    # Display ingredients DataFrame in a formatted table
    # Args: df (pandas DataFrame) - ingredients to display
    if len(df) == 0:
        print(" No ingredients to display.")
        return
    
    # Use pandas to_string for clean table display
    print(df.to_string(index=False))
    print(f"\n Total items: {len(df)}")

def update_ingredient():
    # Update an existing ingredient's quantity
    # Uses: pandas filtering, user input validation
    print("\n=== ✏ Update Ingredient ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found to update.")
        return
    
    # Show current ingredients for reference
    print("\nCurrent ingredients:")
    print(ingredients[['id', 'name', 'quantity', 'unit']].to_string(index=False))
    
    # Get ingredient ID to update
    while True:
        try:
            ingredient_id = int(input("\nEnter ingredient ID to update: "))
            # Check if ID exists
            if ingredient_id in ingredients['id'].values:
                break
            else:
                print(" Ingredient ID not found. Please try again.")
        except ValueError:
            print(" Please enter a valid number for ID.")
    
    # Get current ingredient info
    current_ingredient = ingredients[ingredients['id'] == ingredient_id].iloc[0]
    print(f"\nCurrent ingredient: {current_ingredient['name']}")
    print(f"Current quantity: {current_ingredient['quantity']} {current_ingredient['unit']}")
    
    # Get new quantity
    while True:
        try:
            new_quantity = float(input("Enter new quantity: "))
            if new_quantity < 0:
                print(" Quantity cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print(" Please enter a valid number for quantity.")
    
    # Update the quantity
    ingredients.loc[ingredients['id'] == ingredient_id, 'quantity'] = new_quantity
    
    # Save changes
    save_ingredients(ingredients)
    
    print(f" Updated {current_ingredient['name']} quantity to {new_quantity} {current_ingredient['unit']}")

def remove_ingredient():
    # Remove an ingredient from the database
    # Uses: pandas filtering, user confirmation
    print("\n===  Remove Ingredient ===")
    
    # Load ingredients
    ingredients = load_ingredients()
    
    if len(ingredients) == 0:
        print(" No ingredients found to remove.")
        return
    
    # Show current ingredients for reference
    print("\nCurrent ingredients:")
    print(ingredients[['id', 'name', 'quantity', 'unit']].to_string(index=False))
    
    # Get ingredient ID to remove
    while True:
        try:
            ingredient_id = int(input("\nEnter ingredient ID to remove: "))
            # Check if ID exists
            if ingredient_id in ingredients['id'].values:
                break
            else:
                print(" Ingredient ID not found. Please try again.")
        except ValueError:
            print(" Please enter a valid number for ID.")
    
    # Get ingredient info for confirmation
    ingredient_to_remove = ingredients[ingredients['id'] == ingredient_id].iloc[0]
    
    # Confirm removal
    print(f"\nAre you sure you want to remove:")
    print(f"ID: {ingredient_to_remove['id']}")
    print(f"Name: {ingredient_to_remove['name']}")
    print(f"Quantity: {ingredient_to_remove['quantity']} {ingredient_to_remove['unit']}")
    
    confirmation = input("\nType 'yes' to confirm removal: ").strip().lower()
    
    if confirmation == 'yes':
        # Remove the ingredient (keep all rows except the one with matching ID)
        ingredients = ingredients[ingredients['id'] != ingredient_id]
        
        # Save changes
        save_ingredients(ingredients)
        
        print(f" Removed {ingredient_to_remove['name']} from inventory.")
    else:
        print(" Removal cancelled.")

def ingredient_management_menu():
    # Main menu for ingredient management features
    # Uses: while loop, if-elif-else, function calls
    while True:
        print("\n" + "="*50)
        print(" INGREDIENT MANAGEMENT")
        print("="*50)
        print("1. Add New Ingredient")
        print("2. View Ingredients")
        print("3. Update Ingredient Quantity")
        print("4. Remove Ingredient")
        print("5. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_ingredient()
        elif choice == "2":
            view_ingredients()
        elif choice == "3":
            update_ingredient()
        elif choice == "4":
            remove_ingredient()
        elif choice == "5":
            print(" Returning to main menu...")
            break
        else:
            print(" Invalid choice! Please enter a number between 1-5.")

# Test function for development
if __name__ == "__main__":
    # This runs only when the file is executed directly
    print("Testing Ingredient Management Module...")
    ingredient_management_menu()
