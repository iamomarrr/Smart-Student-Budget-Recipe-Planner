# Smart Student Budget & Recipe Planner System Design

In our first version, a student enters a grocery budget and the ingredients they already have. The planner finds three different dinners for one person and shows which whole packages to buy. This is the central user story in our [requirements](03-requirements.md).

## Main screen

Our [main-screen sketch](ui-sketch.png) puts the budget, pantry rows, and photo upload on the left. The right side shows three dinners, the packages to buy, the estimated total, and how much money is left. If the student uploads a photo, they can check the suggestions and enter how much of each ingredient they have.

## Architecture

| Component | Responsibility |
| --- | --- |
| Web page and form handling | Collect the budget and pantry amounts. Check that the budget is zero or more and that each chosen ingredient has a whole number greater than zero in the unit shown. Show the plan, photo suggestions, or a message about what to fix. |
| Recipe and price catalog | Hold the one-serving recipes, ingredient units, pack sizes, and sample prices. The prototype reads this information from files when it starts. |
| Dinner planner | Try each group of three different recipes and pick the cheapest group that fits the budget. Report when no group fits. |
| Basket pricing | Add up the ingredients needed for all three dinners. Subtract what the student already has from that total. Work out how many whole packages to buy and add up their prices. |
| Photo adapter and Gemini | Prepare the photo and ask Gemini to suggest ingredients from our list. Send the suggestions to the web page for the student to check. If the photo step fails, send a message so the student can continue by hand. |

Our working prototype uses Flask for the web page and Python for the planner and cost calculations. We are checking which language the final MVP should use.

## Design pattern

We use the **Adapter** pattern to connect the photo feature to Gemini. Our photo component makes the image smaller and saves it as a JPEG before sending it. It reads the suggestions Gemini sends back, keeps ingredients from our list, and removes repeats. The student checks the suggestions and enters the amounts. The Adapter gives our app a simple list of ingredients to work with, making it easier to use a different photo service later.

## Planner design alternatives

| Question | Price meals individually | Price each three-dinner basket |
| --- | --- | --- |
| How do we choose meals? | Work out what each dinner costs on its own and pick the three cheapest. | Work out the shopping total for each set of three different dinners and pick the cheapest set that fits the budget. |
| How do we count pantry ingredients and packages? | Each dinner uses the same starting pantry amounts. This can count ingredients already at home twice or add the price of the same package twice. | Add the amounts needed for all three dinners, subtract what the student has, and buy enough whole packages for the rest. |
| How many prices do we calculate? | One price per recipe. | With eight recipes, we price 56 groups of three. The starter catalog is small enough to check every group. |

We chose to price all three dinners together because the student pays for one shopping trip. In the sample plan, the chickpea pasta and chickpea rice each need 120 g of chickpeas. Pricing them separately counts two 240 g packs for NIS 11.00. Together they need one pack for NIS 5.50. With the sample pantry and a NIS 30.00 budget, the full shopping list costs NIS 22.50 and leaves NIS 7.50.

## UML diagrams

| Diagram | What to check |
| --- | --- |
| [Use case diagram](diagrams/use-case.png) | Shows what a student can do. They can add or edit pantry items, find a dinner plan, and get ingredient suggestions from a photo with Gemini. |
| [Class diagram](diagrams/class.png) | Shows how a plan connects to three recipes and one shopping list. Each item on the list records the amount needed, the amount the student already has, and the number of packs to buy. |
| [Sequence diagram](diagrams/sequence.png) | Follows the steps after a student asks for a plan. It shows what happens when a plan fits and when the budget is too low. |

## Decision and task allocation

| Work | Who will do it | What we will do |
| --- | --- | --- |
| Proposal and planner design | Omar Kadan | Check that the proposal matches our first version. Explain how the planner works and why we chose to price three dinners together. Check that the sample plan fits at NIS 22.50 and shows a low-budget message at NIS 22.49. |
| Class and sequence diagrams | Omar Kadan and Obida Jbara | Omar will show how our recipes, ingredients, and shopping list are connected in the class diagram. Obida will check both budget cases in the sequence diagram and update it based on what he finds. |
| Requirements and backlog | Obida Jbara | Review and improve our three user stories and their acceptance tests. Set up our task list with priorities and link it in the requirements. Check that adding 3 tomatoes and 2 onions to the sample pantry brings the total to NIS 11.50. |
| Pantry and photo design | Obida Jbara | Explain how our photo feature works and why we chose the Adapter pattern. Update the use case diagram and screen sketch. Check that students can review photo suggestions and enter their own amounts. |
| README | Omar Kadan and Obida Jbara | Omar describes what the app does and how it works, then adds links to the design and the three diagrams. Obida describes who the app serves and how students use it, then adds links to the proposal, requirements, screen sketch, and backlog. We check each other's sections and links. |

We will open pull requests for our own changes and review each other's work. Omar will check the requirements and photo design. Obida will check the planner design and both budget cases. We will record what we checked and what changed in our reviews.

## AI use and checks

We used OpenAI Codex (GPT-5) to help write this design and make the diagram images. The example totals match the working prototype. We will check the design and diagrams against our requirements and record our checks in the pull request reviews. Our prototype uses Gemini (`gemini-3.5-flash-lite`) for photo suggestions. We will prepare ingredient photos and check whether Gemini's suggestions match what's in each photo before students try the app.
