"""
Authors: Nancy Xing 
Assignment: CSCI 3725 PQ2 (Adapted from PQ1)
Date: 9-25-2023

The Recipe class models a recipe as a list of ingredients with specified amounts. 
Recipes are created by either reading from file, reading from a file directory,
or providing a name and a dict of Ingredient objects keyed by category. Recipes can be written to a text file. 
"""

from typing import *
from .ingredient import Ingredient
from .constants import *


class Recipe:
    def __init__(self, recipe_name: str = None, ingredients: dict[str, List[Ingredient]] = {}) -> None:
        """Initialize recipe with optional name and ingredients.

        name -- name of the recipe 
        ingredients -- List of ingredient objects in the recipe in the format: {category : [Ingredients]}
        """
        self.recipe_name = recipe_name
        self.ingredients = {}

        # Initialize dict with all passed values or empty list if not found
        for c in CATEGORIES:
            self.ingredients.update({c: ingredients.get(c, [])})

    def get_recipe_name(self) -> str:
        """Return recipe name."""
        return self.recipe_name

    def get_recipe_ingredients(self) -> dict[str, List[Ingredient]]:
        """Return all recipe ingredients ordered by category."""
        return self.ingredients

    def get_ingredients_in_category(self, category: str) -> List[Ingredient]:
        """Return all recipe ingredients in one category."""
        return self.ingredients.get(category, [])

    def add_ingredient(self, category: str, ingredient: str) -> None:
        """Add existing ingredient to recipe. Does not matter if ingredient category is already in recipe."""
        category_list = self.ingredients.get(category)
        if category_list != None:
            category_list.append(ingredient)

    def __str__(self) -> str:
        """
        Serializes the recipe with format:
        Recipe Name: [name]
        [ingredient]
        [ingredient]...
        """
        ingredients = ""
        for cat, ings in self.ingredients.items():
            for i in ings:
                ingredients += f"{str(i)}\n"
        serialize = f"Recipe Name: {self.recipe_name}\n{ingredients}"
        return serialize


if __name__ == "__main__":
    # Initial dictionary where not all category is filled
    test_dict = {
        DRY_BASES: [Ingredient("Flour", 1, OUNCE)],
        WET_BASES: [Ingredient("Butter", 1, CUP), Ingredient("Eggs", 2, "")],
        SWEETENERS: [Ingredient("Sugar", 1, CUP)],
        SPICES: [Ingredient("Corriander", 1.5, TSP)]
    }
    r = Recipe(recipe_name="Test Recipe", ingredients=test_dict)

    r.add_ingredient(SPICES, Ingredient("Salt", 1, TSP)
                     )  # Add ing to existing category
    # Add ing to new category
    r.add_ingredient(FILLINGS, Ingredient("Chocolate", 3, TBSP))

    print(str(r))
