import os
import pandas as pd

class DietAnalyzer:
    def __init__(self, data_path):
        """Load and initialize the dataset."""
        self.df = pd.read_csv(data_path)
        # Clean data: remove any recipes with 0 for all macros
        self.df = self.df[(self.df['Protein(g)'] > 0) | 
                          (self.df['Carbs(g)'] > 0) | 
                          (self.df['Fat(g)'] > 0)]

    def get_summary_by_diet(self):
        """Returns average macronutrients per diet type."""
        summary = self.df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
        return summary.round(2)

    def find_culturally_inclusive_meals(self, diet, target_macro, min_amount, max_amount=None):
        """
        Finds recipes for a specific diet that meet a macro-nutrient goal,
        ensuring results show the diverse cuisines available.
        """
        # Filter by diet
        filtered = self.df[self.df['Diet_type'].str.lower() == diet.lower()]
        
        # Filter by macro target
        if target_macro not in ['Protein(g)', 'Carbs(g)', 'Fat(g)']:
            raise ValueError("Macro must be 'Protein(g)', 'Carbs(g)', or 'Fat(g)'")
            
        filtered = filtered[filtered[target_macro] >= min_amount]
        if max_amount:
            filtered = filtered[filtered[target_macro] <= max_amount]
            
        # Sort by the target macro
        results = filtered.sort_values(by=target_macro, ascending=False)
        
        # Return Recipe name, Cuisine, and the Macros to highlight diversity
        return results[['Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']]

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
