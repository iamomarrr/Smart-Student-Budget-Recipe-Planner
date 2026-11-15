# Smart Student Budget & Recipe Planner

**Team members**

* Omar Kadan   : (id on fourm)
* Obida Jbara  : (id on fourm)

## 1. Problem and need

Our target users are college students who cook for themselves and shop with a fixed grocery budget. Before a grocery trip, they have to decide what to cook, check what they already have, and work out what the missing ingredients will cost. A recipe can look cheap per serving while still requiring the student to pay for several full packages. The need is a quick way to decide what to cook and know how much money the next grocery trip will require.

## 2. Proposed solution

We propose a web app that takes a grocery spending limit and the ingredients and amounts a student already has. It returns three one-serving dinners, the ingredients to buy for all three, the estimated total, and the budget left. Python combines ingredient needs across the meals, deducts the confirmed pantry amounts, and prices the missing quantities in sellable packages from a dated store catalog. It chooses the lowest-cost combination among the recipes it checks and tells the student when it finds no combination within the cap.

For example, if the dinners use 500 g of rice and the student has 200 g, the grocery list needs to cover 300 g. If a 1 kg bag is the available package at NIS 8, the estimated grocery spend for rice is NIS 8. A planned photo or screenshot upload will help students enter their pantry items faster.

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

- **MVP.** We chose three dinners because that is enough to test whether meals can share grocery packages while keeping the first version manageable. The form will start with three pantry rows and let students add more. If a student enters five relevant ingredients from the catalog, the planner will account for all five when calculating what to buy.
- **Suitable meal combination.** A plan must include three different one-serving recipes from the checked starter catalog. Every required quantity must be covered by the pantry or the shopping list, and the total cost of the packs must fit the budget. The planner then picks the cheapest combination that meets those rules.

## 7. Feasibility, constraints, and risks

Three people can build the first version around a Python planner, a small Flask web interface, and a catalog of common ingredients with one known package size and price per ingredient. We can use store prices collected on a specific date and review the starter recipes by hand. The main constraints are one semester, team time for gathering prices and testing recipes, and the cost and availability of any AI service we choose.

| Risk | How we will handle it |
| --- | --- |
| A store price changes | Display the store and date with the estimate and use the same price snapshot for repeatable tests. |
| Few recipes fit a tight budget | Try representative student budgets early and use the pilot results to decide where the recipe catalog needs more variety. |
| Photo recognition gives wrong results or the AI service is unavailable | Put suggestions on a review screen and keep manual entry available. |
| Students prefer their current workflow | Give them the same planning task and record where they spend time or correct the output. |

## 8. Business model and AI use

We propose a free course pilot. It creates value by saving planning time and helping students decide what they can buy. We will measure the effort of maintaining the catalog and the cost of hosting and AI calls before considering wider use.

- **AI role.** A vision-capable model can suggest pantry items from a photo or screenshot. Later, an AI agent could propose meals with catalog ingredient IDs and amounts that the Python planner can check against the budget.
- **Verification.** Students confirm each detected item and its quantity. We will compare the detector against sample images with a known list of ingredients. Recipe suggestions must use supported ingredients and usable quantities before they reach the planner.
- **Cost.** After choosing a provider, we will estimate the cost per photo or recipe request and track the number of requests in the pilot. The first version can run with checked recipes and manual entry.
- **Data and privacy.** The app will process an upload for detection and discard its copy after the request. The planner needs the confirmed ingredients and their amounts. We will check the provider’s retention policy and use staged ingredient photos or screenshots for testing.

## 9. Open questions

- Which store and product sizes best represent the way our target students shop?
- What spending caps and recipes do the first students consider realistic for three dinners?
- How accurately can the photo feature recognize catalog ingredients in a cluttered fridge or a screenshot, and does it save time after corrections?
- Which AI provider fits the pilot’s cost and response-time limits, and how does it handle uploaded images?
