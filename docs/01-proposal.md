# Smart Student Budget & Recipe Planner

**Team members**

* Omar Kadan   : (id on fourm)
* Obida Jbara  : (id on fourm)

## 1. Problem and need

Our target users are college students who cook for themselves and shop with a fixed grocery budget. Before a grocery trip, they have to decide what to cook, check what they already have, and work out what the missing ingredients will cost. A recipe can look cheap per serving while still requiring the student to pay for several full packages. The need is a quick way to decide what to cook and know how much money the next grocery trip will require.

## 2. Proposed solution

We propose a web app that takes a grocery budget and the ingredients and amounts a student already has. It returns three one-serving dinners, a combined shopping list, the estimated total, and the budget left. The planner combines ingredient needs across the meals, deducts the pantry amounts, and prices what is missing in whole packages. It picks the cheapest combination in the starter catalog that fits the budget and reports when none fits. The current prototype uses sample package sizes and prices.

For example, if the dinners use 500 g of rice and the student has 200 g, the grocery list needs to cover 300 g. If rice comes in 1 kg bags at NIS 8, the estimate includes one bag at NIS 8. The prototype also accepts a photo or screenshot and suggests pantry ingredients. The student reviews the suggestions and enters the quantities.

## 3. Users and stakeholders

| Context | Stakeholder | What they need |
| --- | --- | --- |
| Product | Students planning their own meals | Dinners they would cook and a shopping list they can check against their budget. |
| Product | Catalog maintainer | A simple way to update recipes, pack sizes, and prices. |
| Course project | Project team | A manageable scope and a clear way to test the demo. |
| Course project | Course instructor | A clear first version and evidence that the team tested it. |

## 4. Current approach and alternatives

We expect some students to browse recipes, check their fridge, and estimate the shopping total by hand or in the store app. We will ask pilot participants how they plan now before we use that workflow as a baseline.

| Alternative | What it offers |
| --- | --- |
| Samsung Food+ | Scans ingredients into a Food List and suggests recipes that use ingredients the student already has. [Samsung Food+ feature guide](https://support.samsungfood.com/hc/en-us/articles/32709269852052-What-s-Included-in-Your-Samsung-Food-Subscription) |
| Budget Bytes | Explains how it estimates recipe costs by pricing the quantity used in each recipe, such as half a package of pasta. [Budget Bytes costing method](https://www.budgetbytes.com/how-to-calculate-recipe-costs/) |

Our reason to switch is a hypothesis. For a student planning several meals at once, a single list that uses their pantry amounts and shows the price of the packages they need to buy should make it easier to commit to a budget. We will compare the same three-dinner task against the students’ usual planning methods and record the time and steps it takes to get a usable list.

## 5. Goal, objectives, and metrics

Our goal is to help students plan dinners they would actually cook and check the estimated cost before shopping. These are our proposed targets for the final MVP demo.

| Objective | Proposed target and measurement |
| --- | --- |
| Make a usable plan quickly | At least four out of five students finish within two minutes. Start timing when the student opens a blank form with a budget and a written pantry list. Include entering the ingredients and quantities, reviewing the dinners and shopping list, and deciding whether they would cook the meals. |
| Improve on the student's usual method | Each student tries both methods on comparable tasks using the same price catalog. Count how many produce three dinners they would cook and a complete shopping list within budget. Our proposed target is a median completion time at least 25% lower with the app among students who finish both tasks, with at least as many successful plans. |
| Verify budget calculations | Match the expected result in all 12 hand-checked scenarios. Include five pantry ingredients, shared packages, a basket exactly at the cap, and a budget too low for any available plan. |

## 6. First version and its boundaries

- **MVP.** Three dinners let us test how meals can share whole grocery packages within a small recipe catalog. The form starts with three pantry rows and lets students add more. If a student enters five ingredients from the catalog, the planner accounts for all five.
- **Suitable meal combination.** A plan includes three different one-serving recipes from the checked starter catalog. The confirmed pantry and shopping list must cover every required amount, and the total pack cost must fit the budget. The planner picks the cheapest combination that meets those rules.
- **Assumption and test.** Students can find three dinners they would cook and a complete shopping list within budget faster than with their usual method. We will test this with the timed comparison and hand-checked scenarios in [Section 5](#5-goal-objectives-and-metrics).
- **Later versions.** Weekly meal plans, dietary filters, and AI-generated recipes.
- **Outside the product's scope.** Grocery checkout, delivery, and medical nutrition advice.

## 7. Feasibility, constraints, and risks

The current prototype uses a Python planner, a small Flask web interface, and one sample pack size and price per ingredient. The small catalog makes it feasible for two-person team to check recipes and costs by hand within the semester. The pilot still needs a dated store price snapshot, time to test recipes with students, and AI usage within the available quota.

| Risk | How we will handle it |
| --- | --- |
| A store price changes | Display the store and date with the estimate and use the same price snapshot for repeatable tests. |
| Few recipes fit a tight budget | Try representative student budgets early and use the pilot results to decide where the recipe catalog needs more variety. |
| Photo recognition gives wrong results or the AI service is unavailable | Let students review suggested pantry rows and keep manual entry available. |
| Students prefer their current workflow | Give them the same planning task and record where they spend time or correct the output. |

## 8. Business model and AI use

We propose a free course pilot. It creates value by saving planning time and helping students decide what they can buy. We will measure the effort of maintaining the catalog and the cost of hosting and AI calls before considering wider use.

- **AI role.** The prototype uses Gemini (`gemini-3.5-flash-lite`) to suggest ingredients from the catalog. The planner computes costs using the pantry quantities the student enters.
- **Verification.** We will compare suggestions against staged images with known contents and record the time students spend correcting suggestions and entering amounts.
- **Cost.** We will estimate cost per photo request and track request counts during the pilot. Manual entry is available for the full planning flow.
- **Data and privacy.** The app sends Gemini a resized copy with image metadata removed. We will check the provider’s retention policy before the pilot and test with staged ingredient photos or screenshots containing invented data.

## 9. Open questions

- Which store and product sizes best represent the way our target students shop?
- What spending caps and recipes do the first students consider realistic for three dinners?
- How accurately can the photo feature recognize catalog ingredients in a cluttered fridge or a screenshot, and does it save time after corrections?
- What cost and response time should we expect from Gemini during the pilot, and what is its image retention policy?
- Does the course require a specific language for the final MVP?
