from src.recipe_generator import RecipeGenerator
from src.quiz import Quiz

if __name__ == "__main__":
    quiz = Quiz()
    generator_request = quiz.run_quiz()
    # print(f"\nRecipe name = {generator_request.get_recipe_name()}")
    # print(f"Created multiplers =\n {generator_request.get_multipliers()}")
    # print(f"Evaluation metric = {generator_request.get_evaluation_metric()}\n")
    recipe_gen = RecipeGenerator(generator_request.get_multipliers())
    recipe = recipe_gen.make_eval_recipe(
        generator_request.get_recipe_name(),
        generator_request.get_evaluation_metric())
    # print(f"score = {recipe.get_eval_score()}")
