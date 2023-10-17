"""
@author: Yonas Gebregziabher

Given probability across the different required components 
of a cookie recipe, selects an amount for each ingredient. 
"""

from .ingredient import Ingredient
from .recipe import Recipe
from typing import List
from .constants import SWEETENERS, FATS, SALTS, LEAVENERS, CUP, OUNCE, TSP, TBSP
import json
import os
import random


class RecipeGenerator:

    def __init__(self, category_probabilities: dict) -> None:
        """
        Initialize ingredient database and user-given category probabilities. 
        """
        self.category_probabilities = category_probabilities
        ing_file = open(os.path.join("assets", "ing_database.json"))
        self.ing_db = json.load(ing_file)

    def set_category_probabilities(self,
                                   category_probabilities: dict[str, float]) -> None:
        """
        Sets user-given category probabilities. 
        """
        self.category_probabilities = category_probabilities

    def get_category_probabilities(self) -> dict:
        """
        Returns user-given category probabilities. 
        """
        return self.category_probabilities

    def generate_ing_amounts(self, unit: str, category: str,
                             num_ings: int) -> List[float]:
        """
        Randomly generate an amount for the ingredient category. Different
        units will be multiplied by numbers from an appropriate range. 
        """
        total_category_amount = 0

        if unit == "oz":
            total_category_amount = round(random.randint(
                1, 9) * self.category_probabilities[category], 1)
        if unit == "cup":
            total_category_amount = round(random.randint(
                1, 4) * self.category_probabilities[category], 1)
        if unit == "tsp":
            total_category_amount = round(random.uniform(
                1, 2) * self.category_probabilities[category], 1)
        if unit == "tbsp":
            total_category_amount = round(random.uniform(
                1, 3) * self.category_probabilities[category], 1)

        if num_ings == 1:
            return [total_category_amount]
        # for ing in ing_list:
        amount_segments = []
        amounts = []
        for i in range(num_ings - 1):
            amount_segments.append(
                round(random.uniform(0.1, total_category_amount), 1))
        amount_segments.append(total_category_amount)
        amount_segments.append(0)
        amount_segments = sorted(amount_segments)

        # two pointers
        for i in range(1, len(amount_segments)):
            amount_diff = amount_segments[i] - amount_segments[i-1]
            amount = max(0.1, round(amount_diff, 1))
            amounts.append(amount)
        return amounts

    def populate_categories_ingredients(self) -> dict[str, List[Ingredient]]:
        """
        Generates ingredients. The ingredient amounts generated are 
        influenced by the category probabilities. 
        """
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
            ing_unit = selected_ing_objs[0]["unit"]
            ing_amounts = self.generate_ing_amounts(
                ing_unit, category, len(selected_ing))

            for i in range(len(selected_ing_objs)):
                ing = selected_ing_objs[i]
                ings.append(Ingredient(ing["name"], ing_amounts[i], ing_unit))

            ingredients[category] = ings
        return ingredients

    def recipe_comparator(self, recipe: Recipe):
        return recipe.get_eval_score()

    def make_eval_recipe(self, name: str, evaluation_metric: str,
                         max_recipes: int = 5) -> Recipe:
        """
        Generate multiple recipes, then return the best one according to the 
        evaluation metric.
        """
        recipes = []
        for _ in range(max_recipes):
            ingredients = self.populate_categories_ingredients()
            recipe = Recipe(name, ingredients)
            reciped_scored = self.get_evaluation_score(
                recipe, evaluation_metric)
            recipes.append(reciped_scored)
        recipes_sorted = sorted(
            recipes, key=self.recipe_comparator, reverse=True)
        return recipes_sorted[0]

    def get_evaluation_score(self, recipe: Recipe,
                             evaluation_metric: str) -> Recipe:
        """
        Computes an evaluation score using the category indicated by the user. 
        Returns recipe with modified score. 
        """
        eval_categories = [FATS, SWEETENERS, SALTS, LEAVENERS]
        if not (evaluation_metric in eval_categories):
            # Invalid evaluation metric
            print("Invalid evaluation metric: " + evaluation_metric)
            recipe.set_eval_score(-1)
            return -1

        category_db = self.ing_db[evaluation_metric]
        ings_list = recipe.get_recipe_ingredients()[evaluation_metric]
        ing_names = [ing["name"] for ing in category_db]
        ing_scores = []

        # Get evaluation score for individual ingredients in category
        for ing in ings_list:
            ing_name = ing.get_ingredient_name()  # name of recipe ingredient
            if ing_name in ing_names:
                flavor_score = 0
                ing_tbsp_amount = 0
                for db_ing in category_db:
                    if db_ing["name"] == ing_name:
                        flavor_score = db_ing["flavor_score"]
                        ing_tbsp_amount = self.convert_to_tbsp(
                            ing.get_ingredient_amount(), db_ing["unit"])

                ing_scores.append(flavor_score * ing_tbsp_amount)

        # Sum ingredient scores
        if len(ing_scores) < 1:
            score = 0
        else:
            score = sum(ing_scores)
        recipe.set_eval_score(score)
        return recipe

    def convert_to_tbsp(self, amount: float, unit: str) -> float:
        """
        Convert given ingredient amount to tablespoons.
        """
        if unit == CUP:
            return amount * 16
        elif unit == OUNCE:
            return amount * 2
        elif unit == TSP:
            return amount * (1/3)
        elif unit == TBSP:
            return amount
        else:
            print("Invalid unit: " + unit)
            return amount
