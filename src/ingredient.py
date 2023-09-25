"""
Authors: Nancy Xing 
Assignment: CSCI 3725 PQ2 (Adapted from PQ1)
Date: 9-25-2023

The Ingredients class models an ingredient as an ingredient name, amount, and unit. 
"""

class Ingredient:
    def __init__(self, ing_name: str, ing_amount: int | float, ing_unit: str) -> None:
        """Initialize ingredient with required name and amount."""
        self.ing_name = ing_name
        self.ing_amount = ing_amount
        self.ing_unit = ing_unit

    def get_ingredient_name(self) -> str:
        """Return ingredient name."""
        return self.ing_name

    def get_ingredient_amount(self) -> int | float:
        """Return ingredient amount."""
        return self.ing_amount
    
    def get_ingredient_unit(self) -> str:
        """Return ingredient unit."""
        return self.ing_unit
    
    def set_ingredient_amount(self, amount: int | float) -> None:
        """Change ingredient amount."""
        self.ing_amount = amount
    
    def set_ingredient_name(self, ing_name: str) -> None:
        """Change ingredient name."""
        self.ing_name = ing_name

    def set_ingredient_unit(self, ing_unit: str) -> str:
        """Change ingredient unit."""
        self.ing_unit = ing_unit

    def __str__(self) -> str:
        """
        Serializes the ingredient with format: [amount] oz [ingredient name]
        """
        if self.ing_unit:
            return f"{self.ing_amount} {self.ing_unit} {self.ing_name}"
        return f"{self.ing_amount} {self.ing_name}"

    def __eq__(self, other: object) -> bool:
        """Compare two sets of ingredients. Ingredients are the same if they have the same name, amount, and unit."""
        if not isinstance(other, Ingredient):
            return False
        else:
            return self.ing_amount == other.ing_amount and \
                self.ing_name == other.ing_name and \
                self.ing_unit == other.ing_unit

    def __hash__(self) -> int:
        """Return a hash of the ingredient."""
        return hash((self.ing_name, self.ing_amount))