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
    # Example Usage
    analyzer = DietAnalyzer("../data/All_Diets.csv")
    
    print("--- Average Macros by Diet Type ---")
    print(analyzer.get_summary_by_diet())
    print("\n")
    
    print("--- High Protein Vegan Meals Across Diverse Cuisines ---")
    # Solving the problem of finding high protein (e.g., >30g) vegan meals
    high_protein_vegan = analyzer.find_culturally_inclusive_meals(
        diet='vegan', 
        target_macro='Protein(g)', 
        min_amount=30.0
    )
    print(high_protein_vegan.head(10))
