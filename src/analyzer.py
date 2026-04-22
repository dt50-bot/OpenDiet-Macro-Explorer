import os
import pandas as pd

class DietAnalyzer:
    def __init__(self, data_path, assumed_servings=4):
        """Load and initialize the dataset, creating per-serving columns."""
        self.df = pd.read_csv(data_path)
        self.assumed_servings = assumed_servings
        
        # Clean data: remove any recipes with 0 for all macros
        self.df = self.df[(self.df['Protein(g)'] > 0) | 
                          (self.df['Carbs(g)'] > 0) | 
                          (self.df['Fat(g)'] > 0)]
                          
        # NEW: Create "Per Serving" columns
        self.df['Protein/Srv'] = (self.df['Protein(g)'] / self.assumed_servings).round(1)
        self.df['Carbs/Srv'] = (self.df['Carbs(g)'] / self.assumed_servings).round(1)
        self.df['Fat/Srv'] = (self.df['Fat(g)'] / self.assumed_servings).round(1)

    def get_summary_by_diet(self):
        """Returns average macronutrients PER SERVING by diet type."""
        summary = self.df.groupby('Diet_type')[['Protein/Srv', 'Carbs/Srv', 'Fat/Srv']].mean()
        return summary.round(1)

    def find_culturally_inclusive_meals(self, diet, target_macro, min_amount, max_amount=None):
        """
        Finds recipes based on PER SERVING macronutrients.
        target_macro input should still be 'Protein(g)', 'Carbs(g)', or 'Fat(g)'
        """
        # Map the original column name to our new per-serving column name
        macro_map = {
            'Protein(g)': 'Protein/Srv',
            'Carbs(g)': 'Carbs/Srv',
            'Fat(g)': 'Fat/Srv'
        }
        serving_macro = macro_map[target_macro]
        
        # Filter by diet
        filtered = self.df[self.df['Diet_type'].str.lower() == diet.lower()]
            
        # Filter by the PER SERVING macro amount
        filtered = filtered[filtered[serving_macro] >= min_amount]
        if max_amount:
            filtered = filtered[filtered[serving_macro] <= max_amount]
            
        # Sort by the target macro (highest to lowest)
        results = filtered.sort_values(by=serving_macro, ascending=False)
        
        # Return Recipe name, Cuisine, and the PER SERVING Macros
        return results[['Recipe_name', 'Cuisine_type', 'Protein/Srv', 'Carbs/Srv', 'Fat/Srv']]

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(current_dir, "..", "data", "All_Diets.csv")
    
    analyzer = DietAnalyzer(data_file_path)
    
    print("\n=============================================")
    print(" Welcome to OpenDiet-Macro-Explorer!")
    print("=============================================\n")
    
    diets = analyzer.df['Diet_type'].unique()
    print(f"Supported Diets: {', '.join(diets)}")
    
    user_diet = input("\nEnter a diet type to explore: ").strip().lower()
    
    print("\nAvailable Macros: Protein, Carbs, Fat")
    raw_macro = input("Which macro are you targeting? ").strip().lower()
    
    # --- NEW: Smart Macro Mapping ---
    # This translates whatever the user types into the exact column name!
    if 'protein' in raw_macro:
        user_macro = 'Protein(g)'
    elif 'carb' in raw_macro:
        user_macro = 'Carbs(g)'
    elif 'fat' in raw_macro:
        user_macro = 'Fat(g)'
    else:
        print("\nError: Could not recognize that macro. Defaulting to Protein(g).")
        user_macro = 'Protein(g)'
    # --------------------------------
    
    try:
        user_min = float(input(f"\nEnter the minimum amount of {user_macro} you want: "))
        
        print("\nSearching database...\n")
        custom_results = analyzer.find_culturally_inclusive_meals(
            diet=user_diet, 
            target_macro=user_macro, 
            min_amount=user_min
        )
        
        if custom_results.empty:
            print("No recipes found matching those criteria. Try adjusting your numbers.")
        else:
            print(f"--- Top Culturally Inclusive {user_diet.capitalize()} Meals ---")
            print(custom_results.head(10).to_string(index=False))
            
    except ValueError:
        print("\nError: Please make sure you enter a valid number for the amount (e.g., 50 or 30.5).")
