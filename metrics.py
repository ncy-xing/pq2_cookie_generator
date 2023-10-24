"""
Script that generators 20 recipes and generates a text file of the same
recipe evaluated across all possible evaluation categories. 
"""

from src.recipe_generator import RecipeGenerator
from src.recipe import Recipe

multipliers = {'flour': 1, 'fats': 1.2, 'sweeteners': 1, 'flavorings': 1,
               'salts': 1, 'liquids': 1, 'leaveners': 0.5, 'add-ins': 1.3,
               'stabilizers': 1, 'toppings': 1}
recipe_gen = RecipeGenerator(multipliers)
eval_categories = ["sweeteners", "fats", "leaveners", "salts"]
outcome_categories = ["sweet", "rich", "fluffy", "salty"]


for i in range(20):
    recipe_ings = recipe_gen.populate_categories_ingredients()
    recipe = Recipe(f"recipe_{i}", recipe_ings)
    recipe_str = str(recipe) + "\n"
    for eval_category, outcome in zip(eval_categories, outcome_categories):
        recipe_scored = recipe_gen.get_evaluation_score(recipe, eval_category)
        recipe_str += f"{eval_category}({outcome})-> {recipe_scored.get_eval_score()} \n"
    with open(f"metrics/recipe_{i}.txt", "w") as recipe_file:
        recipe_file.write(recipe_str)
