#!/usr/bin/env python3
# This line tells the computer to use Python 3 to run this file

# Dynamic Recipe & Waste Management System
# Main Entry Point - This is where our program starts running
#
# This is a comprehensive Python project that demonstrates:
# - Basic Python concepts (variables, data types, operators, control structures)
# - Data structures (lists, dictionaries, tuples, sets)
# - File handling and CSV operations
# - Object-oriented programming
# - Machine Learning with sklearn
# - Data visualization with matplotlib
# - Pandas for data manipulation
#
# Author: Student Project
# Course: Fundamentals of Computer Science using Python
# University: Lok Jagruti University

# Import our custom modules from the modules package
# Since we created an __init__.py file in the modules directory,
# Python now recognizes it as a package and we can import from it directly
from modules.menu import main_menu  # Import the main_menu function from modules/menu.py

def main():
    # Main function to start the application
    # This function contains all the startup code for our program

    # Use try-except block to handle errors gracefully
    try:
        # Start the main menu system directly - this calls the function from menu.py
        main_menu()
    except KeyboardInterrupt:
        # This block runs if user presses Ctrl+C to quit the program
        print("\n\nThank you for using our system! Goodbye!")
    except Exception as e:
        # This block runs if any other error occurs
        error_message = f"\nAn error occurred: {e}"  # Create error message
        print(error_message)  # Print the error message
        print("Please contact support or check your data files.")

# This special condition checks if this file is being run directly
# (not imported as a module by another file)
if __name__ == "__main__":
    main()  # Call the main function to start the program
