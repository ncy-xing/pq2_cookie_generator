# from src.ingredient import Ingredient
from numpy import mean
from src.recipe import Recipe
from src.constants import *
import os
import json

OPTION_CHARACTER = 97
DEFAULT_MULTIPLIER = 1.0

#TODO add opening text and answer choice instructions
#TODO add more questions 
#TODO improve error handling on user inputs
def run_questions() -> dict[str, int | float]:
    """
    Reads in questions from JSON file and gets user input for questions. Convert user
    response into associated multiplier for question response. 
    Multiplier defaults to 1 for each category.

    returns: (recipe name, dict of {category name : multiplier})
    """
    # Initialize questions and multipliers
    questions_file = open(os.path.join("assets", "questions.json"))
    questions = json.load(questions_file)
    responses = []
    recipe_name = ""
    multiplier_dict = {}
    for c in CATEGORIES:
        multiplier_dict.update({c : None})

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
        responses.append(response_options[response_choice_index]["responseText"])
        question_multipliers = response_options[response_choice_index]["multipliers"]


        # Add question multiplier to total multipliers 
        for q in question_multipliers:
            for c, m in q.items():
                category_multipliers = multiplier_dict.get(c)
                if category_multipliers:
                    category_multipliers.append(m)
                else:
                    multiplier_dict.update({c : [m]})

    multipliers = {}

    # Average multiple question effects on categories to get single multiplier. Initialize unmultiplied categories to 1. 
    for c, m in multiplier_dict.items():
        if not m:
            multipliers.update({c : DEFAULT_MULTIPLIER})
        elif len(m) == 1:
            multipliers.update({c : m})
        else:
            multipliers.update({c : sum(m) / len(m)})   

    for r in responses:
        recipe_name += f"{r} "
    recipe_name += "Cookie"

    return recipe_name, multipliers

if __name__ == "__main__":
    name, multipliers = run_questions()
    print(f"Recipie name = {name}")
    print(f"Created multiplers = {multipliers}")