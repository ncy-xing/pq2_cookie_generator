# QuizzyByte Baker

### Recipe Generation

In order to guarantee that we at least get something that resembles a cookie,
we designed our program include all the categories that make up a cookie.
This was inspired by the PIERRE soup generation system where they divided
the ingredients up into their respective abstract categories. In doing so,
we get novel cookie recipe that conform to the baseline requirements of a cookie
that doesn't rely on an existing database of recipes to draw inspiration from.

<img width="375" alt="image" src="https://github.com/ncy-xing/pq2_cookie_generator/assets/86376122/c22af3ba-4fe1-4f23-b951-09bca9e4efd5">

### How does QuizzyByte Baker work?

QuizzyByte Baker works by first creating a `GeneratorRequest` object that
contains the multipliers for the different cookie categories. This multiplier
dictionary is populated by the response to the questions that each
impact the dictionary in specific ways, as noted in `assets/questions.json`.
The `Quiz` class is also responsible for determining which category to
evaluate by based on the response to the questions that asks for the desired
cookie outcome.

```
{
'flour': 1, 'fats': 1.2, 'sweeteners': 1, 'flavorings': 1,
 'salts': 1, 'liquids': 1, 'leaveners': 0.5, 'add-ins': 1.3,
 'stabilizers': 1, 'toppings': 1
}
```

Using this multiplier, `RecipeGenerator` then is responsible for making recipes,
as well as evaluating and selecting the best ones.

In `RecipeGenerator`, `populate_categories_ingredients()` uses the multiplier
dictionary above in conjunction with `assets/ing_database.json` to determine
how many ingredients to select for each category and which ingredients to
select. Ingredients are selected based on a probability distribution based on
how common the ingredients are in cookies we normally see. This is done by
design to ensure that we're not falling into mere generation and increasing
the effective usefulness of our system. We want the cookies to be cookies that
are new but still aren't far from the cookies that we see in everyday life,
therefore, we found selecting ingredients based on a weight distribution
to be effective way to achieve this. Next, the ingredient amounts are also
influenced by the multiplier dictionary. For each unit (cup, tbsp, tsp, oz),
there are different baseline ranges. We then generate a number from 1 to the
max range for the unit and multiply it by the category's multiplier amount.
We then maintain the 3, 2, 1 ratio of cookie ingredients by multiplying
the amount that we generated and then using the maximum amount allocated
for that category to split the distribute the ingredients amount with. This
normalization was done to prevent the situations where we have way more quantity
in one category than the others and effectively making the cookie unedible.

### Evaluation

{someone discuss this in great detail here}
