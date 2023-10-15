"""
@author: Yonas Gebregziabher

Given probability across the different required components 
of a cookie recipe, selects an amount for each ingredient. 
"""

from .ingredient import Ingredient
from .recipe import Recipe
from typing import List
import json
import os
import random


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
            return round(random.randint(1, 9) * self.category_probabilities[category], 1)
        if unit == "cup":
            return round(random.randint(1, 4) * self.category_probabilities[category], 1)
        if unit == "tsp":
            return round(random.uniform(1, 2) * self.category_probabilities[category], 1)
        if unit == "tbsp":
            return round(random.uniform(1, 3) * self.category_probabilities[category], 1)

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

    def make_recipe(self, name: str) -> Recipe:
        ingredients = self.populate_categories_ingredients()
        return Recipe(name, ingredients)
