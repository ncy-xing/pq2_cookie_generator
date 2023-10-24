"""
Assignment: CSCI 3725 PQ2
Date: 10-11-2023

The Quiz class readers the quiz questions and their corresponding response
choices to populate a multiplier dictionary for the different cookie
categories. It also determines the evaluation metric category for the cookie 
based on the user's responses.
"""

from .constants import CATEGORIES
from .generator_request import GeneratorRequest
import os
import json

OPTION_CHARACTER = 97
DEFAULT_MULTIPLIER = 1.0


class Quiz():
    def __init__(self) -> None:
        """
        Initialize questions from file and default multipliers for category. 
        """
        questions_file = open(os.path.join("assets", "questions.json"))
        self.questions = json.load(questions_file)
        self.multipliers = {}
        for c in CATEGORIES:
            self.multipliers.update({c: 1})

    def get_question_response(self, questions: dict[str, str | list]) -> int:
        """
        Displays a question and reads in user response. 

        returns: list index of the answer choice selected
        """
        question_text = questions["questionText"]
        response_options = questions["responseOptions"]
        num_options = len(response_options)

        # Print question and answer choices
        print(f"\n{question_text}")
        for i in range(num_options):
            choice_letter = OPTION_CHARACTER + i
            response_text = response_options[i]["responseText"]
            print(f"({(chr(choice_letter).upper())}) {response_text}")

        # Intake user answer
        response = input(f"\nType your choice: ")
        while not self.is_valid_response(response, num_options):
            response = input("Invalid response. Type in a valid letter: ")
        response = response[0].lower()

        # Convert user answer to its associated index
        response_choice_index = ord(response) - OPTION_CHARACTER
        return response_choice_index

    def is_valid_response(self, response: str, num_options: int) -> bool:
        """
        Helper function for get_question_response. 

        returns: true if user inputted a valid response letter if it is one letter
        and within the letter options

        """
        response = response.lower()
        return len(response) == 1 \
            and ord(response) in range(OPTION_CHARACTER, OPTION_CHARACTER +
                                       num_options)

    def run_quiz(self) -> dict[str, int | float]:
        """
        Reads in questions from JSON file and gets user input for questions. 
        Generate a recipe name based on user choices. Computes multipliers for 
        each ingredient category which are impacted by user choices. 
        Multiplier defaults to 1 for each category.

        returns: resonseGenerator object
        """
        responses = []
        recipe_name = ""
        evaluation_metric = ""

        # Load main questions
        print(self.questions["startText"])
        for question in self.questions["questions"]:
            response_choice_index = self.get_question_response(question)
            responses.append(question["responseOptions"]
                             [response_choice_index]["responseText"])
        question_multipliers = question["responseOptions"][response_choice_index]["multipliers"]

        # Add question multiplier to total multipliers
        for q in question_multipliers:
            for c, m in q.items():
                self.multipliers.update({c: self.multipliers.get(c) + m})

        # Load evaluation question. Convert user answer to evaluation metric.
        eval_question = self.questions["evaluationQuestion"]
        response_choice_index = self.get_question_response(eval_question)
        evaluation_metric = eval_question["responseOptions"][response_choice_index]["evaluateBy"]

        # Generate recipe name from responses
        for r in responses:
            recipe_name += f"{r} "
        recipe_name += "Cookies"

        return GeneratorRequest(recipe_name, self.multipliers, evaluation_metric)
