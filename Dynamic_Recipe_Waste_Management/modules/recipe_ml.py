# Feature 2: Recipe Suggestion using Machine Learning
#
# This module uses Decision Tree Classifier to suggest recipes based on available ingredients.
#
# Uses concepts from syllabus:
# - Machine Learning with sklearn
# - Decision Tree Classifier
# - Pandas for data manipulation
# - Binary encoding for ML features
# - Model training and prediction

# Import required libraries (all from syllabus)
import pandas as pd  # For CSV operations and data manipulation
from sklearn.tree import DecisionTreeClassifier  # Machine Learning algorithm
from sklearn.metrics import accuracy_score  # Model evaluation
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

def load_available_ingredients():
    # Load available ingredients from ingredients.csv file
    # This function reads the CSV file and returns only ingredients with quantity > 0
    #
    # Returns: list of available ingredient names
    #
    # Uses syllabus concepts:
    # - Pandas read_csv() function
    # - DataFrame filtering operations
    # - List operations and tolist() method
    try:
        # Get correct file path and read ingredients CSV file using pandas
        ingredients_file = get_data_file_path("ingredients.csv")
        ingredients_df = pd.read_csv(ingredients_file)

        # Filter ingredients with quantity > 0 - break down the operation
        ingredients_with_stock = ingredients_df[ingredients_df['quantity'] > 0]
        available_names = ingredients_with_stock['name']
        available = available_names.tolist()
        return available
    except FileNotFoundError:
        print(" Ingredients file not found.")
        return []  # Return empty list if file not found

def load_ml_dataset():
    # Load the ML dataset for training the Decision Tree model
    # This function loads the binary-encoded dataset for machine learning
    #
    # Returns: features (X), target (y), and complete dataframe
    #
    # Uses syllabus concepts:
    # - Pandas DataFrame operations
    # - drop() method to remove columns
    # - Exception handling with try-except
    try:
        # Get correct file path and read ML dataset CSV file
        ml_file = get_data_file_path("ml_dataset.csv")
        ml_df = pd.read_csv(ml_file)

        # Features (X) are all columns except recipe_name (independent variables)
        X = ml_df.drop('recipe_name', axis=1)

        # Target (y) is recipe_name column (dependent variable)
        y = ml_df['recipe_name']

        return X, y, ml_df
    except FileNotFoundError:
        print(" ML dataset file not found. Generating from recipes...")
        generate_ml_dataset()  # Generate dataset if not found
        return load_ml_dataset()  # Recursive call after generation

def generate_ml_dataset():
    # Generate ML dataset from recipes.csv file
    # Converts ingredient lists to binary encoding for machine learning
    #
    # This function demonstrates:
    # - String operations (split, strip)
    # - Set operations for unique ingredients
    # - List comprehensions and loops
    # - Dictionary creation and manipulation
    # - Pandas DataFrame operations
    try:
        # Get correct file path and load recipes from CSV file
        recipes_file = get_data_file_path("recipes.csv")
        recipes_df = pd.read_csv(recipes_file)

        # Get all unique ingredients from all recipes - use simple loops
        all_ingredients = set()
        for ingredients_str in recipes_df['ingredients']:
            # Split comma-separated ingredients
            ingredients_parts = ingredients_str.split(',')
            # Clean each ingredient and add to set
            for ingredient in ingredients_parts:
                clean_ingredient = ingredient.strip()
                all_ingredients.add(clean_ingredient)

        # Convert set to list and sort for consistent order
        ingredients_list = list(all_ingredients)
        all_ingredients = sorted(ingredients_list)

        # Create binary encoding for each recipe
        ml_data = []  # List to store all recipe data

        # Process each recipe row - break down complex operations
        for _, row in recipes_df.iterrows():
            recipe_name = row['recipe_name']

            # Split ingredients string into list - use simple operations
            ingredients_str = row['ingredients']
            ingredients_parts = ingredients_str.split(',')
            ingredients_list = []
            for ingredient in ingredients_parts:
                clean_ingredient = ingredient.strip()
                ingredients_list.append(clean_ingredient)

            # Create binary vector - use simple if-else instead of ternary
            binary_row = {}
            binary_row['recipe_name'] = recipe_name

            for ingredient in all_ingredients:
                # Check if ingredient is in this recipe
                ingredient_present = False
                for recipe_ingredient in ingredients_list:
                    if ingredient == recipe_ingredient:
                        ingredient_present = True
                        break

                # Set 1 if present, 0 if not
                if ingredient_present:
                    binary_row[ingredient] = 1
                else:
                    binary_row[ingredient] = 0

            # Add this recipe's data to our list
            ml_data.append(binary_row)

        # Create DataFrame from list of dictionaries
        ml_df = pd.DataFrame(ml_data)

        # Save to CSV file using correct path
        ml_file = get_data_file_path("ml_dataset.csv")
        ml_df.to_csv(ml_file, index=False)

        print(" ML dataset generated successfully!")

    except FileNotFoundError:
        print(" Recipes file not found.")

def train_recipe_model():
    # Train Decision Tree Classifier for recipe suggestion
    # This function demonstrates machine learning concepts from syllabus
    #
    # Returns: trained model and feature names
    #
    # Uses syllabus concepts:
    # - Decision Tree Classifier from sklearn
    # - Model training with fit() method
    # - Model evaluation with accuracy_score
    # - Random state for reproducible results
    # Load ML dataset (X = features, y = target)
    X, y, _ = load_ml_dataset()  # We don't need the full dataframe here

    if len(X) == 0:
        print(" No data available for training.")
        return None, None

    # Create Decision Tree Classifier (from syllabus)
    model = DecisionTreeClassifier(
        random_state=42,      # For reproducible results
        max_depth=10,         # Prevent overfitting
        min_samples_split=2   # Minimum samples to split a node
    )

    # Train the model using fit() method
    model.fit(X, y)

    # Calculate training accuracy for evaluation
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)

    print(f" Model trained successfully! Training accuracy: {accuracy:.2%}")

    # Return model and feature names (column names)
    return model, X.columns.tolist()

def suggest_recipes():
    # Main function to suggest recipes based on available ingredients
    print("\n===  AI Recipe Suggestion ===")
    
    # Load available ingredients
    available_ingredients = load_available_ingredients()
    
    if not available_ingredients:
        print(" No ingredients available in stock.")
        return
    
    print(f"\n Available ingredients: {', '.join(available_ingredients)}")
    
    # Train model
    model, feature_names = train_recipe_model()
    
    if model is None:
        print(" Could not train model.")
        return
    
    # Create input vector for prediction with proper feature names
    input_data = {}
    for feature in feature_names:
        # Check if ingredient is available
        if feature in available_ingredients:
            input_data[feature] = 1
        else:
            input_data[feature] = 0

    # Convert to DataFrame with proper feature names to avoid warnings
    import pandas as pd
    input_df = pd.DataFrame([input_data])

    # Get prediction
    try:
        prediction = model.predict(input_df)
        suggested_recipe = prediction[0]

        # Get prediction probabilities for confidence
        probabilities = model.predict_proba(input_df)
        max_prob = max(probabilities[0])
        confidence = max_prob * 100
        
        print(f"\n Suggested Recipe: {suggested_recipe}")
        print(f" Confidence: {confidence:.1f}%")
        
        # Show recipe ingredients
        show_recipe_details(suggested_recipe)
        
        # Check if user can actually make this recipe
        check_recipe_feasibility(suggested_recipe, available_ingredients)
        
    except Exception as e:
        print(f" Error in prediction: {e}")

def show_recipe_details(recipe_name):
    # Show details of a specific recipe
    # This function demonstrates pandas DataFrame filtering and string operations
    #
    # Args: recipe_name (str) - name of the recipe
    #
    # Uses syllabus concepts:
    # - Pandas read_csv() and DataFrame filtering
    # - iloc[] for row selection
    # - String formatting and print operations
    try:
        # Read recipes CSV file using correct path
        recipes_file = get_data_file_path("recipes.csv")
        recipes_df = pd.read_csv(recipes_file)

        # Filter DataFrame to find matching recipe (boolean indexing)
        recipe_row = recipes_df[recipes_df['recipe_name'] == recipe_name]

        if len(recipe_row) > 0:
            # Get ingredients using iloc[] for row selection
            ingredients = recipe_row.iloc[0]['ingredients']
            print(f"\nRecipe Details:")
            print(f"Name: {recipe_name}")
            print(f"Required Ingredients: {ingredients}")
        else:
            print(f" Recipe details not found for {recipe_name}")

    except FileNotFoundError:
        print(" Recipes file not found.")

def check_recipe_feasibility(recipe_name, available_ingredients):
    # Check if user has all ingredients needed for the recipe
    # This function demonstrates list operations and string manipulation
    #
    # Args:
    #     recipe_name (str) - name of the recipe
    #     available_ingredients (list) - list of available ingredients
    #
    # Uses syllabus concepts:
    # - List comprehensions and string split() method
    # - For loops and conditional statements
    # - Membership operators (in, not in)
    # - List append() method
    try:
        # Read recipes CSV file using correct path
        recipes_file = get_data_file_path("recipes.csv")
        recipes_df = pd.read_csv(recipes_file)

        # Find the specific recipe
        recipe_row = recipes_df[recipes_df['recipe_name'] == recipe_name]

        if len(recipe_row) > 0:
            # Split ingredients string into list and strip whitespace
            required_ingredients = [ing.strip() for ing in recipe_row.iloc[0]['ingredients'].split(',')]

            # Check which ingredients are missing using loops
            missing_ingredients = []
            for ingredient in required_ingredients:
                # Use membership operator 'not in'
                if ingredient not in available_ingredients:
                    missing_ingredients.append(ingredient)

            # Check if all ingredients are available
            if not missing_ingredients:  # Empty list evaluates to False
                print(" You have all ingredients needed for this recipe!")
            else:
                # Use join() method to create comma-separated string
                print(f" Missing ingredients: {', '.join(missing_ingredients)}")
                print(" Consider buying these ingredients or try a different recipe.")

    except FileNotFoundError:
        print(" Recipes file not found.")

def get_all_possible_recipes():
    # Show all recipes that can be made with current ingredients
    # This function demonstrates advanced list operations and built-in functions
    #
    # Uses syllabus concepts:
    # - all() built-in function
    # - enumerate() function for counting
    # - Dictionary creation and manipulation
    # - List append() method and for loops
    print("\n===  All Possible Recipes ===")

    # Load available ingredients from stock
    available_ingredients = load_available_ingredients()

    if not available_ingredients:
        print(" No ingredients available in stock.")
        return

    try:
        # Read recipes from CSV file using correct path
        recipes_file = get_data_file_path("recipes.csv")
        recipes_df = pd.read_csv(recipes_file)
        possible_recipes = []  # List to store recipes we can make

        # Check each recipe using iterrows() method
        for _, row in recipes_df.iterrows():
            recipe_name = row['recipe_name']
            # Split and clean ingredient names
            required_ingredients = [ing.strip() for ing in row['ingredients'].split(',')]

            # Check if all required ingredients are available using all() function
            can_make = all(ingredient in available_ingredients for ingredient in required_ingredients)

            if can_make:
                # Create dictionary for this recipe
                possible_recipes.append({
                    'recipe': recipe_name,
                    'ingredients': row['ingredients']
                })

        # Display results
        if possible_recipes:
            print(f"\n You can make {len(possible_recipes)} recipe(s):")
            # Use enumerate() to get index and item
            for i, recipe in enumerate(possible_recipes, 1):
                print(f"{i}. {recipe['recipe']}")
                print(f"   Ingredients: {recipe['ingredients']}")
        else:
            print("No complete recipes can be made with current ingredients.")
            print(" Try the AI suggestion for partial matches!")

    except FileNotFoundError:
        print(" Recipes file not found.")

def add_new_recipe():
    # Add a new recipe to the database
    # This function demonstrates user input validation and DataFrame operations
    #
    # Uses syllabus concepts:
    # - input() function for user interaction
    # - String methods: strip(), title()
    # - Membership operators (in)
    # - Conditional statements (if-else)
    # - max() function and DataFrame operations
    # - Dictionary creation and pd.concat()
    print("\n=== ➕ Add New Recipe ===")

    try:
        # Load existing recipes from CSV using correct path
        recipes_file = get_data_file_path("recipes.csv")
        recipes_df = pd.read_csv(recipes_file)

        # Get new recipe details from user
        recipe_name = input("Enter recipe name: ").strip().title()

        # Check if recipe already exists using membership operator
        if recipe_name in recipes_df['recipe_name'].values:
            print(f" Recipe '{recipe_name}' already exists.")
            return

        print("Enter ingredients separated by commas (e.g., Tomato, Onion, Garlic):")
        ingredients = input("Ingredients: ").strip()

        # Validate ingredients input using conditional statement
        if not ingredients:
            print(" Please enter at least one ingredient.")
            return

        # Generate new recipe ID using max() function
        new_id = recipes_df['recipe_id'].max() + 1 if len(recipes_df) > 0 else 1

        # Create new recipe dictionary
        new_recipe = {
            'recipe_id': new_id,
            'recipe_name': recipe_name,
            'ingredients': ingredients
        }

        # Add to DataFrame using pd.concat() (modern pandas approach)
        new_row_df = pd.DataFrame([new_recipe])
        recipes_df = pd.concat([recipes_df, new_row_df], ignore_index=True)

        # Save to CSV file using correct path
        recipes_file = get_data_file_path("recipes.csv")
        recipes_df.to_csv(recipes_file, index=False)

        print(f" Recipe '{recipe_name}' added successfully!")

        # Regenerate ML dataset to include new recipe
        print("Updating ML dataset...")
        generate_ml_dataset()

    except FileNotFoundError:
        print(" Recipes file not found.")

def recipe_suggestion_menu():
    # Main menu for recipe suggestion features
    while True:
        print("\n" + "="*50)
        print(" AI RECIPE SUGGESTION")
        print("="*50)
        print("1. Get AI Recipe Suggestion")
        print("2. View All Possible Recipes")
        print("3. Add New Recipe")
        print("4. Regenerate ML Dataset")
        print("5. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-5): ").strip()
        
        if choice == "1":
            suggest_recipes()
        elif choice == "2":
            get_all_possible_recipes()
        elif choice == "3":
            add_new_recipe()
        elif choice == "4":
            print("🔄 Regenerating ML dataset...")
            generate_ml_dataset()
        elif choice == "5":
            print(" Returning to main menu...")
            break
        else:
            print(" Invalid choice! Please enter a number between 1-5.")

# Test function for development
if __name__ == "__main__":
    print("Testing Recipe Suggestion Module...")
    recipe_suggestion_menu()
