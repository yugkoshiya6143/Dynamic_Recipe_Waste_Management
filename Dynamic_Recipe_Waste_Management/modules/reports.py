# Feature 5: Reports & Analytics
#
# This module generates visual reports and analytics:
# - Ingredient usage reports with bar charts
# - Expense reports with pie charts
# - Waste analysis reports
# - Combined analytics dashboard
#
# Uses concepts from syllabus:
# - Pandas for data manipulation
# - Matplotlib for data visualization
# - Data aggregation and analysis
# - Chart creation and customization

# Import required libraries (all from syllabus)
import pandas as pd  # For CSV operations and data manipulation
import matplotlib.pyplot as plt  # For creating charts and graphs
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

def load_data_for_reports():
    # Load all necessary data files for generating reports
    # Returns: tuple of DataFrames (ingredients, expenses, waste)
    # 
    # Uses syllabus concepts:
    # - Multiple pandas read_csv() operations
    # - Exception handling with try-except
    # - Tuple return values
    
    try:
        ingredients_file = get_data_file_path("ingredients.csv")
        ingredients = pd.read_csv(ingredients_file)
    except FileNotFoundError:
        ingredients = pd.DataFrame()

    try:
        expenses_file = get_data_file_path("expenses.csv")
        expenses = pd.read_csv(expenses_file)
    except FileNotFoundError:
        expenses = pd.DataFrame()

    try:
        waste_file = get_data_file_path("waste.csv")
        waste = pd.read_csv(waste_file)
    except FileNotFoundError:
        waste = pd.DataFrame()
    
    return ingredients, expenses, waste

def ingredient_usage_report():
    # Generate ingredient usage report with bar chart
    # This function demonstrates data visualization with matplotlib
    # 
    # Uses syllabus concepts:
    # - Pandas groupby() for data aggregation
    # - Matplotlib bar chart creation
    # - Chart customization (title, labels, colors)
    
    print("\n===  Ingredient Usage Report ===")
    
    # Load data
    ingredients, expenses, waste = load_data_for_reports()
    
    if len(ingredients) == 0:
        print(" No ingredient data found.")
        return
    
    # Group ingredients by name and sum quantities - break down operations
    grouped_ingredients = ingredients.groupby("name")
    usage = grouped_ingredients["quantity"].sum()

    # Sort by quantity (highest first)
    usage_sorted = usage.sort_values(ascending=False)
    
    # CLI output
    print("\n Current Ingredient Stock:")
    print("-" * 40)
    for ingredient, quantity in usage_sorted.items():
        print(f"{ingredient:<20} {quantity:>8.1f}")
    print("-" * 40)
    print(f"Total ingredients: {len(usage_sorted)}")
    
    # Create bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(usage_sorted.index, usage_sorted.values, color='skyblue', edgecolor='navy')
    
    # Customize chart
    plt.title("Ingredient Usage Report", fontsize=16, fontweight='bold')
    plt.xlabel("Ingredients", fontsize=12)
    plt.ylabel("Quantity", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.show()
    
    print("Bar chart displayed!")

def expense_report():
    # Generate expense report with pie chart
    # This function demonstrates pie chart creation and data analysis
    # 
    # Uses syllabus concepts:
    # - Pandas groupby() and sum() for aggregation
    # - Matplotlib pie chart creation
    # - Percentage calculations and formatting
    
    print("\n===  Expense Report ===")
    
    # Load data
    ingredients, expenses, waste = load_data_for_reports()
    
    if len(expenses) == 0:
        print(" No expense records found.")
        return
    
    # Group expenses by ingredient and sum costs - break down operations
    grouped_expenses = expenses.groupby("name")
    ingredient_wise = grouped_expenses["cost"].sum()
    total_cost = expenses["cost"].sum()

    # Sort by cost (highest first)
    ingredient_wise_sorted = ingredient_wise.sort_values(ascending=False)
    
    # CLI output
    print("\n Expense Breakdown:")
    print("-" * 40)
    for ingredient, cost in ingredient_wise_sorted.items():
        percentage = (cost / total_cost) * 100
        print(f"{ingredient:<20} ₹{cost:>8.2f} ({percentage:>5.1f}%)")
    print("-" * 40)
    print(f"Total Expenses: ₹{total_cost:.2f}")
    
    # Create pie chart
    plt.figure(figsize=(10, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6']
    
    wedges, texts, autotexts = plt.pie(ingredient_wise_sorted.values, 
                                      labels=ingredient_wise_sorted.index,
                                      autopct='%1.1f%%',
                                      colors=colors[:len(ingredient_wise_sorted)],
                                      startangle=90,
                                      explode=[0.05] * len(ingredient_wise_sorted))
    
    # Customize chart
    plt.title("Expense Distribution by Ingredient", fontsize=16, fontweight='bold')
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    plt.show()
    
    print("🥧 Pie chart displayed!")

def waste_analysis_report():
    # Generate waste analysis report
    # This function demonstrates waste data analysis and visualization
    # 
    # Uses syllabus concepts:
    # - Pandas data analysis operations
    # - Multiple chart types (bar and pie)
    # - Data filtering and grouping
    
    print("\n===  Waste Analysis Report ===")
    
    # Load data
    ingredients, expenses, waste = load_data_for_reports()
    
    if len(waste) == 0:
        print(" No waste data found.")
        return
    
    # Analyze waste by reason
    waste_by_reason = waste.groupby("reason")["cost"].sum()
    total_waste_cost = waste["cost"].sum()
    
    # CLI output
    print("\n Waste Analysis:")
    print("-" * 40)
    for reason, cost in waste_by_reason.items():
        percentage = (cost / total_waste_cost) * 100
        print(f"{reason:<15} ₹{cost:>8.2f} ({percentage:>5.1f}%)")
    print("-" * 40)
    print(f"Total Waste Cost: ₹{total_waste_cost:.2f}")
    
    # Create charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart for waste by reason
    bars = ax1.bar(waste_by_reason.index, waste_by_reason.values, 
                   color=['red', 'orange', 'yellow', 'pink', 'purple'][:len(waste_by_reason)])
    ax1.set_title("Waste Cost by Reason", fontweight='bold')
    ax1.set_xlabel("Reason")
    ax1.set_ylabel("Cost (₹)")
    ax1.tick_params(axis='x', rotation=45)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'₹{height:.1f}', ha='center', va='bottom')
    
    # Pie chart for waste distribution
    ax2.pie(waste_by_reason.values, labels=waste_by_reason.index, autopct='%1.1f%%',
            colors=['red', 'orange', 'yellow', 'pink', 'purple'][:len(waste_by_reason)])
    ax2.set_title("Waste Distribution", fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print(" Waste analysis charts displayed!")

def combined_analytics_dashboard():
    # Generate a comprehensive analytics dashboard
    # This function demonstrates advanced data visualization
    # 
    # Uses syllabus concepts:
    # - Multiple subplot creation
    # - Complex data analysis and aggregation
    # - Advanced matplotlib customization
    
    print("\n=== Combined Analytics Dashboard ===")
    
    # Load data
    ingredients, expenses, waste = load_data_for_reports()
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Chart 1: Ingredient Stock (Bar Chart)
    if len(ingredients) > 0:
        usage = ingredients.groupby("name")["quantity"].sum().sort_values(ascending=False)
        ax1.bar(usage.index, usage.values, color='lightblue')
        ax1.set_title("Current Ingredient Stock", fontweight='bold')
        ax1.set_ylabel("Quantity")
        ax1.tick_params(axis='x', rotation=45)
    else:
        ax1.text(0.5, 0.5, 'No ingredient data', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title("Current Ingredient Stock", fontweight='bold')
    
    # Chart 2: Expense Distribution (Pie Chart)
    if len(expenses) > 0:
        expense_by_ingredient = expenses.groupby("name")["cost"].sum()
        ax2.pie(expense_by_ingredient.values, labels=expense_by_ingredient.index, autopct='%1.1f%%')
        ax2.set_title("Expense Distribution", fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'No expense data', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title("Expense Distribution", fontweight='bold')
    
    # Chart 3: Waste by Reason (Bar Chart)
    if len(waste) > 0:
        waste_by_reason = waste.groupby("reason")["cost"].sum()
        ax3.bar(waste_by_reason.index, waste_by_reason.values, color='salmon')
        ax3.set_title("Waste Cost by Reason", fontweight='bold')
        ax3.set_ylabel("Cost (₹)")
        ax3.tick_params(axis='x', rotation=45)
    else:
        ax3.text(0.5, 0.5, 'No waste data', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title("Waste Cost by Reason", fontweight='bold')
    
    # Chart 4: Summary Statistics (Text)
    ax4.axis('off')  # Turn off axis for text display
    
    # Calculate summary statistics
    total_ingredients = len(ingredients) if len(ingredients) > 0 else 0
    total_expenses = expenses["cost"].sum() if len(expenses) > 0 else 0
    total_waste_cost = waste["cost"].sum() if len(waste) > 0 else 0
    
    summary_text = f"""
     SUMMARY STATISTICS
    
     Total Ingredients: {total_ingredients}
     Total Expenses: ₹{total_expenses:.2f}
     Total Waste Cost: ₹{total_waste_cost:.2f}
    
    Efficiency Metrics:
    - Waste Percentage: {(total_waste_cost/total_expenses*100) if total_expenses > 0 else 0:.1f}%
    - Active Ingredients: {total_ingredients}
    """
    
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    
    plt.suptitle("Kitchen Management Analytics Dashboard", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print(" Complete analytics dashboard displayed!")

def generate_text_report():
    # Generate a comprehensive text-based report
    # This function demonstrates data analysis without visualization
    # 
    # Uses syllabus concepts:
    # - Comprehensive data analysis
    # - Statistical calculations
    # - Text formatting and presentation
    
    print("\n=== Comprehensive Text Report ===")
    
    # Load data
    ingredients, expenses, waste = load_data_for_reports()
    
    print("\n" + "="*60)
    print("           KITCHEN MANAGEMENT REPORT")
    print("="*60)
    
    # Ingredients Section
    print("\n INGREDIENT ANALYSIS:")
    if len(ingredients) > 0:
        total_items = len(ingredients)
        total_quantity = ingredients['quantity'].sum()
        avg_quantity = ingredients['quantity'].mean()
        
        print(f"- Total ingredient entries: {total_items}")
        print(f"- Total quantity in stock: {total_quantity:.1f}")
        print(f"- Average quantity per item: {avg_quantity:.1f}")
        
        # Top ingredients by quantity
        top_ingredients = ingredients.groupby('name')['quantity'].sum().sort_values(ascending=False).head(3)
        print(f"- Top ingredients by quantity:")
        for i, (name, qty) in enumerate(top_ingredients.items(), 1):
            print(f"  {i}. {name}: {qty:.1f}")
    else:
        print("- No ingredient data available")
    
    # Expenses Section
    print("\n EXPENSE ANALYSIS:")
    if len(expenses) > 0:
        total_cost = expenses['cost'].sum()
        avg_cost = expenses['cost'].mean()
        num_purchases = len(expenses)
        
        print(f"- Total expenses: ₹{total_cost:.2f}")
        print(f"- Average cost per purchase: ₹{avg_cost:.2f}")
        print(f"- Number of purchases: {num_purchases}")

        # Most expensive ingredients
        expensive_ingredients = expenses.groupby('name')['cost'].sum().sort_values(ascending=False).head(3)
        print(f"- Most expensive ingredients:")
        for i, (name, cost) in enumerate(expensive_ingredients.items(), 1):
            print(f"  {i}. {name}: ₹{cost:.2f}")
    else:
        print("- No expense data available")
    
    # Waste Section
    print("\n WASTE ANALYSIS:")
    if len(waste) > 0:
        total_waste_cost = waste['cost'].sum()
        waste_items = len(waste)
        avg_waste_cost = waste['cost'].mean()
        
        print(f"- Total waste cost: ₹{total_waste_cost:.2f}")
        print(f"- Number of waste entries: {waste_items}")
        print(f"- Average waste cost per item: ₹{avg_waste_cost:.2f}")

        # Waste by reason
        waste_reasons = waste.groupby('reason')['cost'].sum().sort_values(ascending=False)
        print(f"- Waste by reason:")
        for reason, cost in waste_reasons.items():
            print(f"  - {reason}: ₹{cost:.2f}")
        
        # Calculate waste percentage
        if len(expenses) > 0:
            waste_percentage = (total_waste_cost / expenses['cost'].sum()) * 100
            print(f"- Waste percentage of total expenses: {waste_percentage:.1f}%")
    else:
        print("- No waste data available")
    
    print("\n" + "="*60)
    print("              END OF REPORT")
    print("="*60)

def reports_menu():
    # Main menu for reports and analytics features
    # This function demonstrates menu-driven programming
    # 
    # Uses syllabus concepts:
    # - while loop for menu repetition
    # - if-elif-else for menu choices
    # - Function calls and program flow control
    
    while True:
        print("\n" + "="*50)
        print(" REPORTS & ANALYTICS")
        print("="*50)
        print("1. Ingredient Usage Report (Bar Chart)")
        print("2. Expense Report (Pie Chart)")
        print("3. Waste Analysis Report")
        print("4. Combined Analytics Dashboard")
        print("5. Generate Text Report")
        print("6. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-6): ").strip()
        
        if choice == "1":
            ingredient_usage_report()
        elif choice == "2":
            expense_report()
        elif choice == "3":
            waste_analysis_report()
        elif choice == "4":
            combined_analytics_dashboard()
        elif choice == "5":
            generate_text_report()
        elif choice == "6":
            print(" Returning to main menu...")
            break
        else:
            print(" Invalid choice! Please enter a number between 1-6.")

# Test function for development
if __name__ == "__main__":
    # This runs only when the file is executed directly
    print("Testing Reports & Analytics Module...")
    reports_menu()
