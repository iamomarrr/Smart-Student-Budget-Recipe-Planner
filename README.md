# Smart Student Budget & Recipe Planner

A Flask course demo. Enter a grocery budget and three ingredients you already have. The planner returns three one-serving dinners and a priced shopping list. [Read the project proposal](docs/01-proposal.md).

## Run locally

Install Python 3.10 or newer. Extract the ZIP and open a terminal in the folder with `app.py`.

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

**macOS or Linux**

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python app.py
```

Open [localhost on port 5000](http://127.0.0.1:5000). The page loads a calculated example. Change the budget or pantry amounts and select **Find dinner plan** to recalculate.

## Demo walkthrough

The sample has a **NIS 30.00** budget, **200 g rice**, **4 eggs**, and **35 ml cooking oil**. The planner uses 170 g rice, 2 eggs, and 30 ml oil across three dinners. It shares one pack of chickpeas between the chickpea pasta and the chickpea rice. The catalog prices are sample values for the demo.

| Purchase | Pack cost |
| --- | ---: |
| One 240 g pack of drained chickpeas | NIS 5.50 |
| One pack of 3 onions | NIS 5.00 |
| One 500 g pack of pasta | NIS 6.00 |
| One pack of 3 tomatoes | NIS 6.00 |
| **Shopping total** | **NIS 22.50** |

The budget has **NIS 7.50** left. Change the cap to **22.50** and the same plan still fits. Change it to **22.49** and the planner reports that it couldn't find an affordable plan from the sample recipes.

## How it works

`app.py` validates the form and calls `find_plan`. The planner tries every combination of three starter recipes. For each combination, `price_basket` adds the required quantities, subtracts pantry stock once, and rounds each remaining amount up to a whole pack. Prices are kept as integer agorot, with 100 agorot equal to NIS 1. Flask renders the cheapest basket the planner found within the cap.

| Walkthrough owner | Open these files | Explain or show |
| --- | --- | --- |
| Omar Kadan | `planner/shopping_list.py`, `planner/meal_plan.py` | Explain why pricing all three recipes together matters. Show how tomatoes are pooled and how a budget equal to the basket cost is accepted. |
| Obida Jbara | `app.py`, `templates/`, `static/styles.css` | Trace the budget and ingredients from the browser form into Python, then show where the result and validation messages are rendered. |
| Basil Haj Yahia | `data/`, `planner/catalog.py`, `tests/` | Explain how recipes reference catalog IDs and units. Walk through the hand-calculated basket and run the exact-cap and below-cap checks. |

## Run the checks

Use the virtual environment's Python from above, followed by `-m unittest discover -s tests -v`.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

The demo uses manual entry and starter recipes. Photo-assisted entry and AI recipe suggestions are the next features described in the proposal. The initial demo files were drafted with AI assistance.
