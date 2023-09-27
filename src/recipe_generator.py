"""
@author: Yonas Gebregziabher

Given probability across the different required components 
of a cookie recipe, selects an amount for each ingredient. 
"""

from .constants import CATEGORIES
from .ingredient import Ingredient
from .recipe import Recipe
from typing import List
import json
import os
import random


BASE_CUP = 1
BASE_OZ = 2
BASE_TSP = 2


class RecipeGenerator:

    def __init__(self, category_probabilities: dict) -> None:
        self.category_probabilities = category_probabilities
        ing_file = open(os.path.join("assets", "ing_database.json"))
        self.ing_db = json.load(ing_file)

    def set_category_probabilities(self, category_probabilities: dict[str, float]) -> None:
        self.category_probabilities = category_probabilities

    def get_category_probabilities(self) -> dict:
        return self.category_probabilities

    def adjust_for_unit(self, unit: str, category: str) -> int:
        if unit == "oz":
            return BASE_OZ * self.category_probabilities[category]
        if unit == "cup":
            return BASE_CUP * self.category_probabilities[category]
        if unit == "tsp":
            return BASE_TSP * self.category_probabilities[category]

    def populate_categories_ingredients(self) -> dict[str, List[Ingredient]]:
        ingredients = {}
        for category in self.ing_db:
            ing_list = self.ing_db[category]
            num_of_elemts = random.randint(1, 2)
            selected_ings = random.sample(ing_list, num_of_elemts)
            ings = []
            for ing in selected_ings:
                ing_unit = ing["unit"]
                ing_amount = self.adjust_for_unit(ing_unit, category)
                ings.append(Ingredient(ing["name"], ing_amount, ing_unit))
            ingredients[category] = ings
        return ingredients

    def gen_recipe_name(self, ingredients: dict[str, List[Ingredient]]) -> str:
        all_ingredients = [ingredient for ingredient_list in ingredients.values(
        ) for ingredient in ingredient_list]
        sorted_ingredients = sorted(
            all_ingredients, key=lambda ingredient: ingredient.get_ingredient_amount(), reverse=True)
        top_3_ingredients = sorted_ingredients[:2]
        return " ".join([ingredient.get_ingredient_name()
                        for ingredient in top_3_ingredients]) + " cookie recipe"

    def make_recipe(self, name: str, ingredients: dict[str, List[Ingredient]]) -> Recipe:
        if name == None:
            name = self.gen_recipe_name(ingredients)
        return Recipe(name, ingredients)
