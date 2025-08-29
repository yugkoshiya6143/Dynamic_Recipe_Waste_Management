# 🍳 Dynamic Recipe & Waste Management System

A comprehensive Python project demonstrating fundamental computer science concepts through a practical kitchen management application.

## 📋 Project Overview

This system helps users manage their kitchen efficiently by:
- **Managing ingredients** with expiry tracking
- **Suggesting recipes** using AI/Machine Learning
- **Tracking food waste** and providing reduction tips
- **Monitoring expenses** and generating reports
- **Predicting expiry dates** using ML algorithms

## 🎓 Educational Value

This project demonstrates all concepts from the **Fundamentals of Computer Science using Python** syllabus:

### Core Python Concepts
- ✅ Variables, data types, and operators
- ✅ Control structures (if-else, loops)
- ✅ Functions and modular programming
- ✅ Data structures (lists, dictionaries, tuples, sets)
- ✅ String operations and manipulation
- ✅ File handling and CSV operations

### Advanced Concepts
- ✅ **Pandas** for data manipulation and analysis
- ✅ **Scikit-learn** for machine learning (Decision Tree Classifier)
- ✅ **Matplotlib** for data visualization and charts
- ✅ **Datetime** for date handling and calculations
- ✅ Exception handling and error management
- ✅ Object-oriented programming concepts

## 🚀 Getting Started

### Prerequisites
```bash
# Install required libraries
pip install pandas scikit-learn matplotlib
```

### Running the Application
```bash
# Navigate to project directory
cd Dynamic_Recipe_Waste_Management

# Run the main application
python main.py
```

## 📁 Project Structure

```
Dynamic_Recipe_Waste_Management/
├── main.py                 # Main entry point
├── requirements.txt        # Required Python libraries
├── README.md              # This documentation
├── data/                  # CSV databases
│   ├── ingredients.csv    # Ingredient inventory
│   ├── recipes.csv        # Recipe database
│   ├── ml_dataset.csv     # ML training data
│   ├── waste.csv          # Waste tracking
│   ├── expenses.csv       # Expense records
│   └── expiry_dataset.csv # Expiry prediction data
├── modules/               # Feature implementations
│   ├── ingredient.py      # Ingredient management
│   ├── recipe_ml.py       # AI recipe suggestions
│   ├── waste.py           # Waste management
│   ├── expiry_ml.py       # ML expiry prediction
│   ├── expiry.py          # Simple expiry check
│   ├── expense.py         # Expense tracking
│   ├── reports.py         # Analytics & reports
│   └── menu.py            # CLI menu system
└── notebooks/             # Jupyter notebooks (optional)
```

## 🔧 Features

### 1. 🥕 Ingredient Management
- Add new ingredients with expiry dates
- View current stock with filtering options
- Update quantities and remove items
- **Concepts**: Pandas operations, user input validation

### 2. 🤖 AI Recipe Suggestions (Machine Learning)
- Uses Decision Tree Classifier
- Suggests recipes based on available ingredients
- Binary encoding for ML features
- **Concepts**: Scikit-learn, ML algorithms, data preprocessing

### 3. 🗑️ Waste Management
- Track wasted ingredients with reasons
- Calculate waste costs and patterns
- Personalized waste reduction tips
- **Concepts**: Data analysis, groupby operations

### 4. 🔮 Expiry Prediction (AI/ML)
- ML-based expiry prediction
- Considers ingredient type and storage
- Batch processing of ingredients
- **Concepts**: Advanced ML, categorical encoding

### 5. 📅 Simple Expiry Check
- Date-based expiry checking
- Automatic removal of expired items
- Status categorization
- **Concepts**: Datetime operations, boolean indexing

### 6. 💰 Expense Tracker
- Record ingredient costs
- Generate expense summaries
- Track spending patterns
- **Concepts**: Mathematical operations, data aggregation

### 7. 📊 Reports & Analytics
- Visual charts using Matplotlib
- Bar charts, pie charts, dashboards
- Comprehensive text reports
- **Concepts**: Data visualization, statistical analysis

## 💻 Sample Usage

```python
# Example: Adding an ingredient
python main.py
# Choose option 1 (Ingredient Management)
# Choose option 1 (Add New Ingredient)
# Follow the prompts to add ingredients

# Example: Getting recipe suggestions
# Choose option 2 (AI Recipe Suggestions)
# Choose option 1 (Get AI Recipe Suggestion)
# System will suggest recipes based on available ingredients
```

## 📊 Data Files

### ingredients.csv
```csv
id,name,quantity,unit,expiry_date,storage_type,date_added,cost
1,Tomato,500,g,2025-08-25,fridge,2025-08-18,50
```

### recipes.csv
```csv
recipe_id,recipe_name,ingredients
1,Tomato Soup,"Tomato,Onion,Garlic"
```

### expiry_dataset.csv (ML Training Data)
```csv
ingredient_type,days_since_purchase,storage_type,status
Vegetables,1,fridge,Safe
Dairy,7,fridge,Expire Soon
```

## 🎯 Learning Outcomes

After working with this project, students will understand:

1. **Data Manipulation**: Using Pandas for real-world data processing
2. **Machine Learning**: Implementing ML algorithms for practical problems
3. **Data Visualization**: Creating meaningful charts and reports
4. **Software Design**: Building modular, maintainable applications
5. **Problem Solving**: Applying programming concepts to solve real problems

## 🔍 Code Style

- **Beginner-friendly syntax**: Complex operations broken into simple steps
- **No advanced features**: Uses only basic Python constructs from syllabus
- **Clear variable names**: Descriptive names that explain each step
- **Simple control structures**: Basic if-else and for loops instead of advanced syntax
- **Step-by-step operations**: One clear operation per line
- **Well-commented**: Every function explains concepts used
- **Modular design**: Each feature in separate modules
- **Error handling**: Graceful handling of user errors
- **Syllabus-aligned**: Only uses concepts from the course

### 🎓 Simplified Syntax Examples

**Before (Complex):**
```python
name = input("Enter name: ").strip().title()
available = df[df['quantity'] > 0]['name'].tolist()
options = '/'.join(valid_units)
```

**After (Beginner-friendly):**
```python
user_input = input("Enter name: ")
clean_input = user_input.strip()
name = clean_input.title()

ingredients_with_stock = df[df['quantity'] > 0]
available_names = ingredients_with_stock['name']
available = available_names.tolist()

options = ""
for unit in valid_units:
    options = options + unit + "/"
options = options[:-1]  # Remove last slash
```

## 🚀 Extensions

Students can extend this project by:
- Adding more ML algorithms (Random Forest, SVM)
- Implementing a web interface with Flask
- Adding database support (SQLite)
- Creating mobile app integration
- Adding nutrition analysis features

## 📚 References

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Scikit-learn Guide**: https://scikit-learn.org/stable/user_guide.html
- **Matplotlib Tutorials**: https://matplotlib.org/stable/tutorials/index.html

## 👨‍💻 Author

**Student Project**  
Course: Fundamentals of Computer Science using Python  
University: Lok Jagruti University

## 📄 License

This project is created for educational purposes as part of the university curriculum.

---

**Happy Coding! 🐍✨**
