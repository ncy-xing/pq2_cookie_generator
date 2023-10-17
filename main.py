from src.recipe_generator import RecipeGenerator
from src.quiz import Quiz

if __name__ == "__main__":
    quiz = Quiz()
    generator_request = quiz.run_quiz()
    recipe_gen = RecipeGenerator(generator_request.get_multipliers())
    recipe = recipe_gen.make_eval_recipe(
        generator_request.get_recipe_name(),
        generator_request.get_evaluation_metric())
    print(recipe)
