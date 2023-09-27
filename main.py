# from src.ingredient import Ingredient
from numpy import mean
from src.recipe import Recipe
from src.constants import *
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
        multipliers.update({c : None})

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
                category_multipliers = multipliers.get(c)
                if category_multipliers:
                    category_multipliers.append(m)
                else:
                    multipliers.update({c : [m]})

    # Combine multipliers from different questions into a single multiplier per category 
    multipliers = merge_multipliers_in_category(multipliers)

    for r in responses:
        recipe_name += f"{r} "
    recipe_name += "Cookie"

    return recipe_name, multipliers

def merge_multipliers_in_category(multipliers : dict[str : [int | float]]) -> dict[str : int | float]:
    """
    Helper function for run_questions. Averages multiple question effects on categories to get single multiplier. 
    Initialize unmultiplied categories to 1.
    params: 
        --multipliers: {category : [multipliers]}
    returns: 
        {category : multiplier} where multiplier is the average of the list values of the initial dict. 
        Categories with None multipliers are initialized to 1.  
    """
    merged_multipliers = {}
    for c, m in multipliers.items():
        if not m:
            merged_multipliers.update({c : DEFAULT_MULTIPLIER})
        elif len(m) == 1:
            merged_multipliers.update({c : m})
        else:
            merged_multipliers.update({c : sum(m) / len(m)})   
    return merged_multipliers
    
if __name__ == "__main__":
    name, multipliers = run_questions()
    print(f"Recipe name = {name}")
    print(f"Created multiplers = {multipliers}")