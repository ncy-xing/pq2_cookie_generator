# from src.ingredient import Ingredient
from src.recipe import Recipe
from src.constants import *
from src.recipe_generator import RecipeGenerator
import os
import json

OPTION_CHARACTER = 97

# TODO add opening text and answer choice instructions
# TODO add more questions
# TODO handle multiple questions changing probability of one category (currently just replaces it)
# TODO improve error handling on user inputs


def run_questions() -> dict[str, int | float]:
    """
    Reads in questions from JSON file and gets user input for questions. Convert user
    response into associated multiplier for question response. 
    Multiplier defaults to 1 for each category.

    returns: dict of {category name : multiplier}
    """
    # Initialize questions and multipliers
    questions_file = open(os.path.join("assets", "questions.json"))
    questions = json.load(questions_file)
    multipliers = {}
    for c in CATEGORIES:
        multipliers.update({c: 1})

    # Load questions
    for q in questions["questions"]:
        question_text = q["questionText"]
        response_options = q["responseOptions"]
        num_options = len(response_options)

        # Print question and answer choices
        print(question_text)
        for i in range(num_options):
            choice_letter = OPTION_CHARACTER + i
            response_text = response_options[i]["responseText"]
            print(f"({(chr(choice_letter).upper())}) {response_text}")

        # Intake user answer
        response = input(f"\nType your choice: ")
        while len(response) > 1:
            response = input("Invalid response. Type in one letter: ")
        response = response[0].lower()
        while ord(response) not in range(OPTION_CHARACTER, OPTION_CHARACTER + num_options):
            response = input("Invalid response. Type in a valid letter: ")

        # Convert user answer to its associated multiplier
        response_choice_index = ord(response) - OPTION_CHARACTER
        response_multipliers = response_options[response_choice_index]["multipliers"]

        # Apply question multipliers to total multipliers
        for m in response_multipliers:
            multipliers.update(m)
    return multipliers


if __name__ == "__main__":
    multipliers = run_questions()
    rm = RecipeGenerator(multipliers)
    ings = rm.populate_categories_ingredients()
    print(rm.make_recipe(None, ings))
