"""
Script that turns the long `metrics.txt` file into separate recipe files for 
easier and further individual analysis. 
"""

import re

# Read the entire input file
with open('metrics/metrics.txt', 'r') as file:
    data = file.read()

# Split the data into individual recipes
recipes = re.split(r'\n\n', data)

for i, recipe in enumerate(recipes):
    with open(f"metrics/recipe{i}.txt", "w") as recipe_file:
        recipe_file.write(recipe)
