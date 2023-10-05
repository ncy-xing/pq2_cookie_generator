# from src.ingredient import Ingredient
from numpy import mean
from src.recipe import Recipe
from src.constants import *
from src.recipe_generator import RecipeGenerator
import os
import json

OPTION_CHARACTER = 97
DEFAULT_MULTIPLIER = 1.0

def run_questions() -> dict[str, int | float]:
    """
    Reads in questions from JSON file and gets user input for questions. 
    Generate a recipe name based on user choices. Computes multipliers for 
    each ingredient category which are impacted by user choices. 
    Multiplier defaults to 1 for each category.

    returns: (recipe name, dict of {category name : multiplier})
    """
    # Initialize questions and multipliers
    questions_file = open(os.path.join("assets", "questions.json"))
    questions = json.load(questions_file)
    responses = []
    recipe_name = ""
    multipliers = {}
    for c in CATEGORIES:
        multipliers.update({c: 1})

    # Load questions
    print(questions["startText"])
    for q in questions["questions"]:
        question_text = q["questionText"]
        response_options = q["responseOptions"]
        num_options = len(response_options)

        # Print question and answer choices
        print(f"\n{question_text}")
        for i in range(num_options):
            choice_letter = OPTION_CHARACTER + i
            response_text = response_options[i]["responseText"]
            print(f"({(chr(choice_letter).upper())}) {response_text}")

        # Intake user answer
        response = input(f"\nType your choice: ")
        while len(response) > 1 or ord(response) not in range(OPTION_CHARACTER, OPTION_CHARACTER + num_options):
            response = input("Invalid response. Type in a valid letter: ")
        response = response[0].lower()

        # Convert user answer to its associated multiplier
        response_choice_index = ord(response) - OPTION_CHARACTER
        responses.append(response_options[response_choice_index]["responseText"])
        question_multipliers = response_options[response_choice_index]["multipliers"]

        # Add question multiplier to total multipliers 
        for q in question_multipliers:
            for c, m in q.items():
                multipliers.update({c : multipliers.get(c) + m})

    for r in responses:
        recipe_name += f"{r} "
    recipe_name += "Cookies"

    return recipe_name, multipliers
    
if __name__ == "__main__":
    name, multipliers = run_questions()
    print(f"Recipe name = {name}")
    print(f"Created multiplers = {multipliers}")
