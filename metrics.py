"""
Script that turns the long `metrics.txt` file into separate recipe files for 
easier and further individual analysis. 
"""

import re
from src.recipe_generator import RecipeGenerator


def convert_to_recipe(text):
    lines = text.split("\n")[2:]
    print(lines)


# Read the entire input file
with open('metrics/metrics.txt', 'r') as file:
    data = file.read()

# Split the data into individual recipes
recipes = re.split(r'\n\n', data)

convert_to_recipe(recipes[0])
