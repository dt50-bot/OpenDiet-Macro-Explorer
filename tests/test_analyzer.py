import unittest
import pandas as pd
import sys
import os

# Add the src directory to the path so we can import the analyzer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from analyzer import DietAnalyzer

class TestDietAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up the analyzer before each test."""
        # Ensure the path points to your dataset
        self.analyzer = DietAnalyzer("data/All_Diets.csv")

    def test_summary_by_diet(self):
        """Test that the summary returns a DataFrame and is not empty."""
        summary = self.analyzer.get_summary_by_diet()
        self.assertFalse(summary.empty, "Summary should not be empty")
        self.assertIn('Protein(g)', summary.columns, "Missing Protein column")

    def test_find_culturally_inclusive_meals(self):
        """Test the filtering logic for vegan meals."""
        results = self.analyzer.find_culturally_inclusive_meals(
            diet='vegan', 
            target_macro='Protein(g)', 
            min_amount=20.0
        )
        self.assertFalse(results.empty, "Should find at least one high-protein vegan meal")
        # Check that all results actually have at least 20g of protein
        self.assertTrue(all(results['Protein(g)'] >= 20.0))

if __name__ == '__main__':
    unittest.main()
