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
BASE_TBSP = 1.5


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
        if unit == "tbsp":
            return BASE_TBSP * self.category_probabilities[category]

    def populate_categories_ingredients(self) -> dict[str, List[Ingredient]]:
        ingredients = {}
        for category in self.ing_db:
            ing_list = self.ing_db[category]
            weights = [float(ing["p"]) for ing in ing_list]
            num_of_elemts = random.randint(1, 3)
            selected_ings_set_str = set()
            selected_ing_objs = []

            for _ in range(len(ing_list)):
                if (len(selected_ings_set_str) == num_of_elemts):
                    break

                selected_ing = random.choices(ing_list, weights)[0]
                if selected_ing["name"] not in selected_ings_set_str:
                    selected_ings_set_str.add(
                        selected_ing["name"])
                    selected_ing_objs.append(selected_ing)
            ings = []
            for ing in selected_ing_objs:
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
