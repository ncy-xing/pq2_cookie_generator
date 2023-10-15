# from src.ingredient import Ingredient
from numpy import mean
from src.recipe import Recipe
from src.constants import *
from src.recipe_generator import RecipeGenerator
from src.quiz import Quiz
import os
import json

OPTION_CHARACTER = 97
DEFAULT_MULTIPLIER = 1.0

if __name__ == "__main__":
    quiz = Quiz()
    generator_request = quiz.run_quiz()
    print(f"\nRecipe name = {generator_request.get_recipe_name()}")
    print(f"Created multiplers =\n {generator_request.get_multipliers()}")
    print(f"Evaluation metric = {generator_request.get_evaluation_metric()}\n")
    recipe_gen = RecipeGenerator(generator_request.get_multipliers())
    recipe = recipe_gen.make_recipe(generator_request.get_recipe_name())
    print(recipe)
