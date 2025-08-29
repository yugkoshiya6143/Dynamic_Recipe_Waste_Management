
# Feature 4: Expiry Prediction using Machine Learning
#
# This module uses Decision Tree Classifier to predict ingredient expiry status
# based on ingredient type, days since purchase, and storage type.
#
# Uses concepts from syllabus:
# - Machine Learning with sklearn
# - Decision Tree Classifier
# - Pandas for data manipulation
# - Model training and prediction
# - Data preprocessing and encoding

# Import required libraries (all from syllabus)
import pandas as pd  # For CSV operations and data manipulation
from sklearn.tree import DecisionTreeClassifier  # Machine Learning algorithm
from sklearn.metrics import accuracy_score  # Model evaluation
from datetime import datetime  # For date calculations
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

def load_expiry_dataset():
    # Load the expiry prediction dataset for training
    # This function loads the dataset with ingredient types and storage info
    # 
    # Returns: features (X) and target (y)
    # 
    # Uses syllabus concepts:
    # - Pandas read_csv() function
    # - DataFrame operations
    # - Exception handling with try-except
    try:
        # Read expiry dataset CSV file using correct path
        expiry_file = get_data_file_path("expiry_dataset.csv")
        expiry_df = pd.read_csv(expiry_file)
        
        # Features (X) are ingredient_type, days_since_purchase, storage_type
        # We need to encode categorical variables to numbers for ML
        
        # Create a copy for processing
        processed_df = expiry_df.copy()
        
        # Encode ingredient_type to numbers - use simple approach
        ingredient_mapping = {}
        ingredient_mapping['Vegetables'] = 1
        ingredient_mapping['Dairy'] = 2
        ingredient_mapping['Grains'] = 3

        # Create new column with encoded values
        encoded_ingredient_types = []
        for ingredient_type in processed_df['ingredient_type']:
            encoded_value = ingredient_mapping[ingredient_type]
            encoded_ingredient_types.append(encoded_value)
        processed_df['ingredient_type_encoded'] = encoded_ingredient_types

        # Encode storage_type to numbers - use simple approach
        storage_mapping = {}
        storage_mapping['fridge'] = 1
        storage_mapping['freezer'] = 2
        storage_mapping['pantry'] = 3

        # Create new column with encoded values
        encoded_storage_types = []
        for storage_type in processed_df['storage_type']:
            encoded_value = storage_mapping[storage_type]
            encoded_storage_types.append(encoded_value)
        processed_df['storage_type_encoded'] = encoded_storage_types
        
        # Features (X) are the encoded columns and days_since_purchase
        X = processed_df[['ingredient_type_encoded', 'days_since_purchase', 'storage_type_encoded']]
        
        # Target (y) is the status column
        y = processed_df['status']
        
        return X, y, processed_df
        
    except FileNotFoundError:
        print(" Expiry dataset file not found.")
        return None, None, None

def train_expiry_model():
    # Train Decision Tree Classifier for expiry prediction
    # This function demonstrates machine learning model training
    # 
    # Returns: trained model and feature names
    # 
    # Uses syllabus concepts:
    # - Decision Tree Classifier from sklearn
    # - Model training with fit() method
    # - Model evaluation with accuracy_score
    # - Data preprocessing
    
    # Load expiry dataset
    X, y, processed_df = load_expiry_dataset()
    
    if X is None:
        print(" No data available for training.")
        return None, None
    
    # Create Decision Tree Classifier
    model = DecisionTreeClassifier(
        random_state=42,      # For reproducible results
        max_depth=5,          # Prevent overfitting
        min_samples_split=3   # Minimum samples to split a node
    )
    
    # Train the model using fit() method
    model.fit(X, y)
    
    # Calculate training accuracy for evaluation
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    
    print(f" Expiry prediction model trained! Training accuracy: {accuracy:.2%}")
    
    # Return model and feature names
    feature_names = ['ingredient_type_encoded', 'days_since_purchase', 'storage_type_encoded']
    return model, feature_names

def predict_ingredient_expiry():
    # Main function to predict expiry status of an ingredient
    # This function demonstrates user interaction and ML prediction
    # 
    # Uses syllabus concepts:
    # - User input with input() function
    # - Data validation and error handling
    # - Dictionary mapping for encoding
    # - Machine learning prediction
    
    print("\n===  Predict Ingredient Expiry ===")
    
    # Train model
    model, feature_names = train_expiry_model()
    
    if model is None:
        print(" Could not train model.")
        return
    
    # Get user input for prediction
    print("\nEnter ingredient details for expiry prediction:")
    
    # Get ingredient type with validation - use simple loops
    ingredient_types = ['Vegetables', 'Dairy', 'Grains']

    # Create types text using simple loop
    types_text = ""
    for ingredient_type_option in ingredient_types:
        types_text = types_text + ingredient_type_option + ", "
    types_text = types_text[:-2]  # Remove last comma and space
    print(f"Available ingredient types: {types_text}")

    ingredient_type = ""
    while True:
        user_type = input("Enter ingredient type: ")
        clean_type = user_type.strip()
        ingredient_type = clean_type.title()

        # Check if type is valid using simple loop
        type_found = False
        for valid_type in ingredient_types:
            if ingredient_type == valid_type:
                type_found = True
                break

        if type_found:
            break
        else:
            print(f" Please enter a valid ingredient type: {types_text}")
    
    # Get days since purchase with validation
    days_since = 0
    while True:
        try:
            user_days = input("Enter days since purchase: ")
            days_since = int(user_days)
            if days_since < 0:
                print(" Days cannot be negative. Please try again.")
            else:
                break  # Exit loop if days is valid
        except ValueError:
            print(" Please enter a valid number for days.")

    # Get storage type with validation - use simple loops
    storage_types = ['fridge', 'freezer', 'pantry']

    # Create storage types text using simple loop
    storage_text = ""
    for storage_option in storage_types:
        storage_text = storage_text + storage_option + ", "
    storage_text = storage_text[:-2]  # Remove last comma and space
    print(f"Available storage types: {storage_text}")

    storage_type = ""
    while True:
        user_storage = input("Enter storage type: ")
        clean_storage = user_storage.strip()
        storage_type = clean_storage.lower()

        # Check if storage type is valid using simple loop
        storage_found = False
        for valid_storage in storage_types:
            if storage_type == valid_storage:
                storage_found = True
                break

        if storage_found:
            break
        else:
            print(f" Please enter a valid storage type: {storage_text}")
    
    # Encode the inputs for prediction (same mapping as training)
    ingredient_mapping = {
        'Vegetables': 1,
        'Dairy': 2,
        'Grains': 3
    }
    
    storage_mapping = {
        'fridge': 1,
        'freezer': 2,
        'pantry': 3
    }
    
    # Create input vector for prediction
    ingredient_encoded = ingredient_mapping[ingredient_type]
    storage_encoded = storage_mapping[storage_type]
    
    # Create input DataFrame with proper feature names to avoid warnings
    input_data = {
        'ingredient_type_encoded': [ingredient_encoded],
        'days_since_purchase': [days_since],
        'storage_type_encoded': [storage_encoded]
    }
    input_df = pd.DataFrame(input_data)

    # Make prediction
    try:
        prediction = model.predict(input_df)
        predicted_status = prediction[0]

        # Get prediction probabilities for confidence
        probabilities = model.predict_proba(input_df)
        max_prob = max(probabilities[0])
        confidence = max_prob * 100
        
        # Display results
        print(f"\n Prediction Results:")
        print(f"Ingredient: {ingredient_type}")
        print(f"Days since purchase: {days_since}")
        print(f"Storage: {storage_type}")
        print(f"Predicted Status: {predicted_status}")
        print(f"Confidence: {confidence:.1f}%")
        
        # Provide recommendations based on prediction
        if predicted_status == 'Safe':
            print(" This ingredient is safe to use!")
        elif predicted_status == 'Expire Soon':
            print(" This ingredient will expire soon. Use it quickly!")
            print(" Consider using it in today's cooking.")
        else:  # Expired
            print(" This ingredient has likely expired. Do not use!")
            print(" Consider disposing of it safely.")
        
    except Exception as e:
        print(f" Error in prediction: {e}")

def check_current_ingredients_expiry():
    # Check expiry status of all current ingredients in stock
    # This function demonstrates batch prediction and data analysis
    # 
    # Uses syllabus concepts:
    # - Pandas DataFrame operations
    # - Date calculations with datetime
    # - Loops and conditional statements
    # - Machine learning batch prediction
    
    print("\n===  Check All Ingredients Expiry ===")
    
    # Train model
    model, feature_names = train_expiry_model()
    
    if model is None:
        print(" Could not train model.")
        return
    
    try:
        # Load current ingredients using correct path
        ingredients_file = get_data_file_path("ingredients.csv")
        ingredients_df = pd.read_csv(ingredients_file)
        
        if len(ingredients_df) == 0:
            print(" No ingredients found in stock.")
            return
        
        # Calculate days since purchase for each ingredient
        today = datetime.today().date()

        # Convert date_added to datetime for calculation
        ingredients_df['date_added'] = pd.to_datetime(ingredients_df['date_added']).dt.date

        # Calculate days since purchase (no .dt needed since we're working with date objects)
        ingredients_df['days_since_purchase'] = (today - ingredients_df['date_added']).apply(lambda x: x.days)
        
        # Map ingredient names to types (simplified mapping)
        name_to_type = {
            'Tomato': 'Vegetables', 'Onion': 'Vegetables', 'Garlic': 'Vegetables', 'Lemon': 'Vegetables',
            'Potato': 'Vegetables', 'Carrot': 'Vegetables', 'Spinach': 'Vegetables',
            'Cheese': 'Dairy', 'Milk': 'Dairy', 'Butter': 'Dairy',
            'Rice': 'Grains', 'Bread': 'Grains'
        }
        
        # Create predictions for each ingredient
        predictions = []
        
        for _, row in ingredients_df.iterrows():
            ingredient_name = row['name']
            days_since = row['days_since_purchase']
            storage_type = row['storage_type']
            
            # Get ingredient type from mapping
            ingredient_type = name_to_type.get(ingredient_name, 'Vegetables')  # Default to Vegetables
            
            # Encode for prediction
            ingredient_mapping = {'Vegetables': 1, 'Dairy': 2, 'Grains': 3}
            storage_mapping = {'fridge': 1, 'freezer': 2, 'pantry': 3}
            
            ingredient_encoded = ingredient_mapping[ingredient_type]
            storage_encoded = storage_mapping[storage_type]
            
            # Make prediction with proper DataFrame to avoid warnings
            input_data = {
                'ingredient_type_encoded': [ingredient_encoded],
                'days_since_purchase': [days_since],
                'storage_type_encoded': [storage_encoded]
            }
            input_df = pd.DataFrame(input_data)
            prediction = model.predict(input_df)[0]
            
            predictions.append({
                'name': ingredient_name,
                'type': ingredient_type,
                'days_since_purchase': days_since,
                'storage': storage_type,
                'predicted_status': prediction,
                'quantity': row['quantity'],
                'unit': row['unit']
            })
        
        # Display results grouped by status
        safe_items = [p for p in predictions if p['predicted_status'] == 'Safe']
        expire_soon_items = [p for p in predictions if p['predicted_status'] == 'Expire Soon']
        expired_items = [p for p in predictions if p['predicted_status'] == 'Expired']
        
        print(f"\n Expiry Analysis Results:")
        print(f"Total ingredients analyzed: {len(predictions)}")
        
        if safe_items:
            print(f"\n Safe items ({len(safe_items)}):")
            for item in safe_items:
                print(f"  - {item['name']} ({item['quantity']} {item['unit']}) - {item['days_since_purchase']} days old")
        
        if expire_soon_items:
            print(f"\n Expire Soon ({len(expire_soon_items)}):")
            for item in expire_soon_items:
                print(f"  - {item['name']} ({item['quantity']} {item['unit']}) - {item['days_since_purchase']} days old")
            print(" Use these ingredients in your next meal!")
        
        if expired_items:
            print(f"\n Likely Expired ({len(expired_items)}):")
            for item in expired_items:
                print(f"  - {item['name']} ({item['quantity']} {item['unit']}) - {item['days_since_purchase']} days old")
            print(" Consider disposing of these items safely.")
        
    except FileNotFoundError:
        print(" Ingredients file not found.")
    except Exception as e:
        print(f" Error in analysis: {e}")

def expiry_prediction_menu():
    # Main menu for expiry prediction features
    # This function demonstrates menu-driven programming
    # 
    # Uses syllabus concepts:
    # - while loop for menu repetition
    # - if-elif-else for menu choices
    # - Function calls and program flow control
    
    while True:
        print("\n" + "="*50)
        print(" EXPIRY PREDICTION (AI/ML)")
        print("="*50)
        print("1. Predict Single Ingredient Expiry")
        print("2. Check All Current Ingredients")
        print("3. View Expiry Dataset")
        print("4. Back to Main Menu")
        print("="*50)
        
        choice = input(" Enter your choice (1-4): ").strip()
        
        if choice == "1":
            predict_ingredient_expiry()
        elif choice == "2":
            check_current_ingredients_expiry()
        elif choice == "3":
            view_expiry_dataset()
        elif choice == "4":
            print(" Returning to main menu...")
            break
        else:
            print(" Invalid choice! Please enter a number between 1-4.")

def view_expiry_dataset():
    # Display the expiry dataset used for training
    # This function demonstrates data viewing and analysis
    
    print("\n===  Expiry Dataset ===")
    
    try:
        # Load and display the dataset using correct path
        expiry_file = get_data_file_path("expiry_dataset.csv")
        expiry_df = pd.read_csv(expiry_file)
        
        print("\nExpiry prediction dataset:")
        print(expiry_df.to_string(index=False))
        
        # Show some statistics
        print(f"\n📈 Dataset Statistics:")
        print(f"Total records: {len(expiry_df)}")
        print(f"Ingredient types: {', '.join(expiry_df['ingredient_type'].unique())}")
        print(f"Storage types: {', '.join(expiry_df['storage_type'].unique())}")
        print(f"Status distribution:")
        status_counts = expiry_df['status'].value_counts()
        for status, count in status_counts.items():
            print(f"  - {status}: {count} records")
        
    except FileNotFoundError:
        print(" Expiry dataset file not found.")

# Test function for development
if __name__ == "__main__":
    # This runs only when the file is executed directly
    print("Testing Expiry Prediction Module...")
    expiry_prediction_menu()
