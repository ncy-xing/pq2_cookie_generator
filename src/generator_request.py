"""
Authors: Nancy Xing 
Assignment: CSCI 3725 PQ2 (Adapted from PQ1)
Date: 10-11-2023

The GeneratorRequest class models a group of input information to pass into 
the RecipeGenerator class consisting of the name of the final recipe, 
multipliers for each category of ingredient, and a metric
by which to evaluate and select generated ingredients. 
"""


class GeneratorRequest():
    def __init__(self, recipe_name: str = "None",
                 multipliers: dict[str, int | float] = {},
                 evaluation_metric: str = None) -> None:

        self.recipe_name = recipe_name
        self.multipliers = multipliers
        self.evaluation_metric = evaluation_metric

    def get_recipe_name(self) -> str:
        """Return recipe name."""
        return self.recipe_name

    def get_multipliers(self) -> dict[str, int | float]:
        """Return recipe multipliers for its respective category."""
        return self.multipliers

    def get_evaluation_metric(self) -> str:
        """Return recipe evaluation metric."""
        return self.evaluation_metric
