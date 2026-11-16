# Smart Student Budget & Recipe Planner Requirements

The first version helps one student plan three one-serving dinners using a grocery budget and ingredients they already have. Prices are sample whole-package prices in NIS. The pilot measures for planning time and cost accuracy are in the [project proposal](01-proposal.md#5-goal-objectives-and-metrics).

## User stories and acceptance tests

### 1. Plan three dinners within budget (central story)

**As a** student with a grocery budget, **I want** a three-dinner plan that uses the pantry quantities I enter, **so that** I know what to buy and whether I can afford it.

Use the starter catalog and a sample pantry of **200 g rice, 4 eggs, and 35 ml cooking oil** for these checks.

| Check | Action | Expected result |
| --- | --- | --- |
| Plan within budget | Enter a budget of NIS 30.00 and request a plan. | The planner shows three different one-serving dinners. The shopping list has one 240 g pack of drained chickpeas, one pack of 3 onions, one 500 g pack of pasta, and one pack of 3 tomatoes. The chickpea pack covers two dinners. The total is NIS 22.50 and NIS 7.50 remains. |
| Accept the exact budget | Change the budget to NIS 22.50 and recalculate. | The plan fits. The shopping total is NIS 22.50 and the remaining budget is NIS 0.00. |
| Handle a budget below the lowest cost | Change the budget to NIS 22.49 and recalculate. | The planner reports that it cannot find three dinners within the budget. The student can adjust the budget or pantry and try again. |
| Validate the budget | Enter a negative budget and try to calculate a plan. | The planner prompts the student to enter a budget of zero or more. |

### 2. Enter and adjust pantry quantities

**As a** student who has ingredients at home, **I want** to add ingredients and correct what I enter, **so that** the shopping list reflects what I actually need to buy.

| Check | Action | Expected result |
| --- | --- | --- |
| Use more than three ingredients | With the sample pantry and NIS 30.00, add rows for 3 tomatoes and 2 onions and request a plan. | The budget and the first three inputs are preserved. The planner uses all five entries. The shopping list contains one pack of drained chickpeas and one pack of pasta, costing NIS 11.50 in total and leaving NIS 18.50. |
| Remove an accidental row | With the sample pantry, add a fourth row by mistake and select **Remove** on that row. | The extra row disappears. The original three pantry entries and budget are still in the form. |
| Leave a row unused | Add a fully blank fourth row to the sample pantry and request a plan with NIS 30.00. | The planner skips the blank row and returns the sample shopping total of NIS 22.50. |
| Complete a selected ingredient | Choose tomatoes in a new row, leave its quantity blank, and try to calculate. | The planner asks for a positive whole amount for that row. The student can enter the amount and retry. |

### 3. Get pantry suggestions from a photo

**As a** student with a photo or screenshot of ingredients, **I want** the app to suggest supported pantry items for me to review, **so that** I can enter what I have faster.

| Check | Action | Expected result |
| --- | --- | --- |
| Suggest ingredients for review | With photo analysis available, start with the sample pantry and NIS 30.00. Upload a clear staged image of tomatoes and onions and select **Analyze photo**. Use JPG, PNG, or WebP up to 10 MB. | Tomatoes and onions appear as editable pantry suggestions with blank quantities. The budget and existing rows are preserved. After checking the suggestions, entering 3 tomatoes and 2 onions, and requesting a plan, the shopping total is NIS 11.50. |
| Reject an invalid image | Submit a small text file named `pantry.jpg` while the sample pantry is filled in. | The planner shows an image error and preserves the pantry entries and budget. |
| Continue without photo setup | Submit a valid image while photo analysis is unconfigured. | The planner explains what is needed for photo analysis and preserves the budget and pantry entries. The student can use the form to plan manually. |

## Use case for the central story

**Prepare a three-dinner shopping plan.** The actor is a student planning a grocery trip. The starter recipe and sample pack-price catalog is available.

### Main flow

1. The student opens the planner and enters a grocery budget in NIS.
2. The student fills in any relevant pantry ingredients and quantities using the units displayed for each item.
3. The student selects **Find dinner plan**.
4. The planner checks the entries and finds the cheapest set of three different one-serving dinners within the budget. It deducts the pantry quantities and prices the remaining quantities in whole packages across the three meals.
5. The planner displays the dinners, package quantities to buy, shopping total, and remaining budget.

### Alternative flow when the budget is too low

At step 4, every available three-dinner basket costs more than the entered budget. The planner shows that no plan fits. The student can revise the budget or the pantry quantities and return to step 3.

## Backlog

[Shared backlog on GitHub](https://github.com/users/obidadev/projects/3/views/1?visibleFields=%5B"Title"%2C445338137%5D)