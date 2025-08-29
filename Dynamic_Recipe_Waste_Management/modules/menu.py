# CLI Menu System
#
# This module provides the main command-line interface menu system
# that integrates all features of the Dynamic Recipe & Waste Management System
#
# Uses concepts from syllabus:
# - Functions and modular programming
# - while loops for menu repetition
# - if-elif-else for menu choices
# - Import statements and module usage
# - User input and validation

# Import all feature modules from the same package
# Since all modules are in the same directory, we can use relative imports
from .ingredient import ingredient_management_menu
from .recipe_ml import recipe_suggestion_menu
from .waste import waste_management_menu
from .expiry_ml import expiry_prediction_menu
from .expiry import expiry_check_menu
from .expense import expense_tracker_menu
from .reports import reports_menu

def show_welcome_message():
    # Simple welcome message
    print("\n" + "=" * 50)
    print("    KITCHEN MANAGEMENT SYSTEM")
    print("=" * 50)
    print("Welcome! This system helps you manage your kitchen.")
    print("You can track ingredients, get recipes, and reduce waste.")
    print("=" * 50)

def show_main_menu():
    # Simple main menu
    print("\n" + "=" * 40)
    print("         MAIN MENU")
    print("=" * 40)
    print("1. Manage Ingredients")
    print("2. Get Recipe Ideas")
    print("3. Track Food Waste")
    print("4. Check Expiry (AI)")
    print("5. Check Expiry (Simple)")
    print("6. Track Expenses")
    print("7. View Reports")
    print("8. Help")
    print("9. Exit")
    print("=" * 40)

def show_help_information():
    # Simple help information
    print("\n" + "=" * 40)
    print("            HELP")
    print("=" * 40)
    print("1. Ingredients - Add, view, update ingredients")
    print("2. Recipes - Get recipe suggestions")
    print("3. Waste - Track wasted food")
    print("4. Expiry AI - Smart expiry checking")
    print("5. Expiry Simple - Basic date checking")
    print("6. Expenses - Track food costs")
    print("7. Reports - View charts and data")
    print("8. Help - This help screen")
    print("9. Exit - Close the program")
    print("=" * 40)

def get_user_choice():
    # Get user choice
    choice = input("\nEnter choice (1-9): ").strip()
    return choice

def main_menu():
    # Main menu function
    show_welcome_message()

    while True:
        try:
            show_main_menu()
            choice = get_user_choice()

            if choice == "1":
                print("\nOpening Ingredients...")
                ingredient_management_menu()
            elif choice == "2":
                print("\nOpening Recipes...")
                recipe_suggestion_menu()
            elif choice == "3":
                print("\nOpening Waste Tracker...")
                waste_management_menu()
            elif choice == "4":
                print("\nOpening AI Expiry Check...")
                expiry_prediction_menu()
            elif choice == "5":
                print("\nOpening Simple Expiry Check...")
                expiry_check_menu()
            elif choice == "6":
                print("\nOpening Expense Tracker...")
                expense_tracker_menu()
            elif choice == "7":
                print("\nOpening Reports...")
                reports_menu()
            elif choice == "8":
                show_help_information()
            elif choice == "9":
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid choice! Please enter 1-9.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

def quick_start_guide():
    # Simple quick start guide
    print("\n" + "=" * 40)
    print("        QUICK START")
    print("=" * 40)
    print("1. Add ingredients first")
    print("2. Get recipe ideas")
    print("3. Track expenses")
    print("4. Check expiry dates")
    print("5. View reports")
    print("=" * 40)

# Test the menu if this file is run directly
if __name__ == "__main__":
    main_menu()
