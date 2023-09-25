"""
Authors: Yonas Gebregziabher, Nancy Xing, Yi Yang 
Assignment: CSCI 3725 PQ2 (Adapted from PQ1)
Date: 9-25-2023

The Recipe class models a recipe as a list of ingredients with specified amounts. 
Recipes are created by either reading from file, reading from a file directory,
or providing a name and a list of Ingredient objects. Recipes can be written to a text file. 
"""

from typing import *
from .ingredient import Ingredient
from constants import *

class Recipe:
    def __init__(self, recipe_name: str = None, ingredients: dict[str, List[Ingredient]] = {}) -> None:
        """Initialize recipe with optional name and ingredients.

        name -- name of the recipe 
        ingredients -- List of ingredient objects in the recipe in the format: {category : [Ingredients]}
        """
        self.recipe_name = recipe_name
        self.ingredients = ingredients #TODO remove
        
        self.dry_bases = ingredients.get(DRY_BASES, None)
        self.wet_bases = ingredients.get(WET_BASES, None)
        self.sweeteners = ingredients.get(SWEETENERS, None)
        self.flavorings = ingredients.get(FLAVORINGS, None)
        self.spices = ingredients.get(SPICES, None)
        self.fillings = ingredients.get(FILLINGS, None)
        self.leaveners = ingredients.get(LEAVENERS, None)
        self.toppings = ingredients.get(TOPPINGS, None)

    def get_recipe_name(self) -> str:
        """Return recipe name."""
        return self.recipe_name

    #TODO
    def get_recipe_ingredients(self) -> List[Ingredient]:
        """Return recipe ingredients."""
        return self.ingredients

    #TODO
    def add_ingredient(self, ingredient: str) -> None:
        """Add existing ingredient to recipe."""
        self.ingredients.append(ingredient)

    #TODO
    def add_ingredient(self, name: str, amount: int | float) -> None:
        """Create a new ingredient and add it to the recipe."""
        self.ingredients.append(Ingredient(
            ingredient_name=name, ingredient_amount=amount))
    
    #TODO
    def __str__(self) -> str:
        """
        Serializes the recipe with format:
        Recipe Name: [name]
        [ingredient]
        [ingredient]...
        """
        ingredients = ""
        for ingredient in self.ingredients:
            ingredients += str(ingredient)
        serialize = f"Recipe Name: {self.recipe_name}\n{ingredients}"
        return serialize
