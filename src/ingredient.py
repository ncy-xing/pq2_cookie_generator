"""
Authors: Yonas Gebregziabher, Nancy Xing, Yi Yang 
Assignment: CSCI 3725 PQ2 (Adapted from PQ1)
Date: 9-25-2023

The Ingredients class models an ingredient as an ingredient name with a specified amount in ounces. 
"""


class Ingredient:
    def __init__(self, ingredient_name: str, ingredient_amount: int | float) -> None:
        """Initialize ingredient with required name and amount."""
        self.ingredient_name = ingredient_name
        self.ingredient_amount = ingredient_amount

    def get_ingredient_name(self) -> str:
        """Return ingredient name."""
        return self.ingredient_name

    def get_ingredient_amount(self) -> int | float:
        """Return ingredient amount."""
        return self.ingredient_amount
    
    def set_ingredient_amount(self, amount: int | float) -> None:
        """Change ingredient amount."""
        self.ingredient_amount = amount
    
    def set_ingredient_name(self, ingredient_name: str) -> None:
        """Change ingredient name."""
        self.ingredient_name = ingredient_name

    def __str__(self) -> str:
        """
        Serializes the ingredient with format: [amount] oz [ingredient name]
        """
        return f"{self.ingredient_amount} oz {self.ingredient_name}"

    def __eq__(self, other: object) -> bool:
        """Compare two sets of ingredients. Ingredients are the same if they have the same name and amount."""
        if not isinstance(other, Ingredient):
            return False
        else:
            return self.ingredient_amount == other.ingredient_amount and \
                self.ingredient_name == other.ingredient_name

    def __hash__(self) -> int:
        """Return a hash of the ingredient."""
        return hash((self.ingredient_name, self.ingredient_amount))