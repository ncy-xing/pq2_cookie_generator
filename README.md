# QuizzyByte Baker

### Recipe Generation

In order to guarantee that we at least get something that resembles a cookie, we modeled our cookie as a combination of ingredients from a set of categories. This was inspired by the PIERRE soup generation system where they divided the ingredients up into their respective abstract categories. In doing so, we get novel cookie recipes that conform to the baseline requirements of a cookie while not relying on an existing database of recipes to draw inspiration
from.

<img width="375" alt="image" src="https://github.com/ncy-xing/pq2_cookie_generator/assets/86376122/c22af3ba-4fe1-4f23-b951-09bca9e4efd5">

### How does QuizzyByte Baker work?

At its core, QuizzyByte offers to create a cookie where all stages of cookie creation, from ingredient to cookie evaluation, are affected by a user’s unique answers to the QuizzyByte quiz.

QuizzyByte Baker works by first asking the user a set of questions which they respond to on the terminal interface. We encoded the first two questions such that a user response to the questions will impact the generation of ingredients based on their category, ie, by applying multipliers to certain categories. (E.g., for the question “How are you feeling today, responding “light” would increase the multiplier for the leavener category.) Each question is encoded to impact specific category multipliers, as noted in `assets/questions.json`. The third question asks users what they look for most in a cookie, which directly translates into the category which will be considered as the base of the evaluation metric.

After the user finishes the quiz, the system formats the response into a `GeneratorRequest` object that contains the input information needed to generate the cookie, including multipliers for the different cookie categories and the final recipe name, and what category to evaluate the cookie off of.

An example set of multipliers which would be passed into RecipeGenerator:

```
{
'flour': 1, 'fats': 1.2, 'sweeteners': 1, 'flavorings': 1,
 'salts': 1, 'liquids': 1, 'leaveners': 0.5, 'add-ins': 1.3,
 'stabilizers': 1, 'toppings': 1
}
```

Using this multiplier, `RecipeGenerator` then is responsible for making a recipe by generating five ingredient lists, computing an evaluation metric for each list, and selecting the best recipe based off of the metric.

In `RecipeGenerator`, `populate_categories_ingredients()` uses the multipliers along with the ingredients found in our ingredient database (`assets/ing_database.json`) to determine
how many ingredients to select for each category and which ingredients to
select. Ingredients are selected based on a probability distribution based on
how common the ingredients are in cookies we normally see. This is done by
design to ensure that we're not falling into mere generation and increasing
the effective usefulness of our system. We want the cookies to be cookies that
are new but still aren't far from the cookies that we see in everyday life,
therefore, we found selecting ingredients based on a weight distribution
to be an effective way to achieve this. Next, the ingredient amounts are also
influenced by the multiplier dictionary. We compute the amounts of ingredients grouping by entire categories. This is done as follows:
Each category uses one unit (cup, tbsp, tsp, oz), and there are different baseline ranges for each unit. Randomly generate the total amount needed in the category (e.g., generate that there should be 2 cups of ingredients total which are sweeteners.)
If there were multiple ingredients generated per category (e.g., a recipe having both sugar and honey), randomly partition this total amount into values for each ingredient.
This method prevents us from stacking ingredients of the same category and having an excess of one category. However, it does not guarantee that categories are still in good proportion to one another. To remedy this, we use the “3 2 1” ratio for cookies, a common baking principle stating the ratio of flours, fats, and sweeteners for a cookie best falls into a 3:2:1 ratio. Our system applies this principle at the end of amount generation by simply adjusting the amount of flour and fats appropriately.

### Types of Creativity

In order to generate a recipe that will be specific to the user's tastes,
`RecipeGenerator` generates five recipes and evaluates them based on the response given to the final question in the quiz: "What do you look for most in a cookie?" This gives the user the ability to choose to evaluate the recipe by the amount of leaveners, sweeteners, salts, or fats. `RecipeGenerator` evaluates each of the generated recipes by the user's chosen metric by comparing the amount of ingredients in the chosen category, taking into account their units and "flavor scores". The function `get_evaluation_score()` totals up the amount of each ingredient and multiplies it by the flavor score to get the final evaluation score. The recipe with the highest evaluation score is considered to be the recipe that fits best with the user's chosen metric, and that recipe is then selected. The system presents the recipe to the user in a readable list of ingredients, with measurement units that make sense for that type of
ingredient.

Out of Jordanous' 14 criteria, our system fits best with the "Social Interaction
and Communication" metric. The quiz gives the user the ability to influence the
recipe generated by creating the multipliers mentioned in the previous section
and by choosing the metric by which the recipes are evaluated. In many ways, the uniqueness of the cookie relies on user communications: first, to bias how the ingredient amounts are generated; second, to determine the criteria in which cookies are selected. The second component is highly evident in our evaluation scoring (metrics folder, generated by metrics.py). `Metrics.py` is a script for us to generate k recipes, in this case hard-coded to 20, where we evaluate the same recipe across all evaluation categories to test the effectiveness of our evaluation algorithm. This tells us the same recipe is not evaluated the same for all desired outcomes. We were able to go through the recipes generated as well as their scores and see how well it scores a recipe respective to its desired outcome. A cookie can score relatively high or relatively low in different categories. The recipe with the highest sweetener score does not necessarily have the highest fats score, and so on for all the categories. Thus, user specification will directly change which cookie is selected.

The second creativity metric that our system focuses on is the "Product" aspect
of the four PPPPerspectives. The generated recipes are very likely to be novel,
since the system does not rely on an inspiring recipe set to influence creation and there is no risk of plagiarism. Our system also prioritizes the value of the product and was intentionally programmed to generate cookie recipes that are useful to humans. It uses multiple mechanisms to achieve this: modeling a cookie as a set of useful categories, generating ingredient amounts in a human-edible range, and making sure the amounts of ingredients stay proportional to each other. The intended audience of our system is anyone who wants a cookie recipe that they can enjoy, so our system will likely be valuable to them, since it is capable of creating cookie recipes that are influenced by the user's tastes.

### Evaluation

Our evaluation methods are inspired by _RecipeGPT: Generative Pre-training Based Cooking Recipe Generation and Evaluation System_, (link)[https://arxiv.org/pdf/2003.02498.pdf] a research done by Helena H. Lee et. al. We adapted the following two components of their system:

- Comparison with reference recipe
- User comments and ratings

Though we didn't have explicit user comments and ratings to influence evaluation, the response to the question that asked what type of cookie they wanted was directly used to influence the metric that we used to evaluate it as
mentioned above.

Additionally, the research paper used comparison with a reference recipe
using ElasticSearch database's ranking ability for the given context.
(Title, ingredient, etc.) Therefore, if the desired context is for example
Nigerian food, it would be further away on the elastic reference search to
Japanese food and closer to typical Nigerian food on the similarity search.
In QuizzyByte Baker's implementation, rather than measuring similarity to the
baseline cookie (since all recipes generated are all cookies), we decided to
determine how similar the cookie is in matching the desired outcome of the
user. In our case, the desired outcome of the user was modeled as a cookie that maximizes the selected category amount.

```
"evaluationQuestion" :
{
"questionText" : "What do you look for most in a cookie?",
"responseOptions" : [
{
"responseText" : "It should be sweet.",
"evaluateBy" : "sweeteners"
},
{
"responseText" : "It should be rich.",
"evaluateBy" : "fats"
},
{
"responseText" : "It should be salty.",
"evaluateBy" : "salts"
},
{
"responseText" : "It should be fluffy.",
"evaluateBy" : "leaveners"
}
]
}
```

If users for example want sweet cookies, we could return the cookie that is
the most similar to a sweet cookie by returning the recipe with the highest
amount of sweeteners. Additionally, ingredients in these categories also have
`flavor_score`. This attribute determines how common/extreme this ingredient
is to its respective category.

```
{
"name": "White Sugar",
"unit": "cup",
"p": 0.4,
"flavor_score": 5
},
{
"name": "Honey",
"unit": "tbsp",
"p": 0.05,
"flavor_score": 7
},
```

This was a much more efficient implementation than assigning a "sweet", "sour", etc. score to the different ingredients because some attributes like sourness are not applicable to all ingredients across all categories. However, since the flavor score is only scored against its category, it is extremely effective. Continuing the example of wanting a sweet cookie, we also use the `flavor_score` to determine evaluation to ensure that we're returning the sweetest cookie that we can. `flavor_score` is effective in addressing the situation where quantity of an ingredient is simply not an accurate measure of sweetness since ingredients like honey, though might come in less quantities, are sweeter than just sugar.

### Determining ingredient data

We needed to generate a database of ingredients for our system to use. We also needed to pre-encode two attributes for each ingredient: the probability of encountering that ingredient (ie, how common it is when baking cookies). For certain categories of ingredients (flour, sweetener, fats, and leaveners), we needed a flavor score for ingredients of those categories to be factored into the evaluation metric.

To create this database, we felt that hand-picking and hand-coding these categories would be insubstantial. However, our team understood we would not be able to implement a sophisticated analysis of flavors and odors given the resource constraints. Our compromise was to generate ingredients and their attributes using ChatGPT. Since ChatGPT is a web-based service, it can reasonably model which ingredients are common (ie, appear on the web often) and infer flavor scores using similar methods. Our prompt given to ChatGPT is copied below. Note that while this prompt may be replicated by different researchers, the resulting ingredients and attributes may be different from the generated ingredients which we used.

Below is our ChatGPT Prompt that gave us the flavor score for each ingredient within the four categories, and the results that ChatGPT gave:

“Given the below JSON, I want you to add a flavor score attribute to each ingredient. This flavor score simply represents its relative flavor value with respect to the other ingredients in the same category. The flavor score should be a value from 1 to 10. For instance, in the sweeteners category, honey is 25% sweeter than white sugar, so it should have a flavor value 1.25 more of the white sugar to represent that. Do this for all the ingredients.”
