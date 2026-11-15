# Smart Student Budget & Recipe Planner

A Flask course demo. Enter a grocery budget and the ingredients you already have. The planner returns three one-serving dinners and a priced shopping list. [Read the project proposal](docs/01-proposal.md).

## Run locally

Install Python 3.10 or newer. Clone the repository or download and extract its ZIP. Open a terminal in the repository root, where this README is located.

**Windows Command Prompt (CMD)**

```cmd
cd smart-student-planner
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

**Windows PowerShell**

```powershell
cd smart-student-planner
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

**macOS or Linux**

```bash
cd smart-student-planner
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python app.py
```

Open [localhost on port 5000](http://127.0.0.1:5000). The page loads a calculated example. Change the budget or pantry amounts and select **Find dinner plan** to recalculate.

## Photo or screenshot upload

Manual pantry entry works immediately. To enable **Analyze photo**, create an API key in [Google AI Studio](https://aistudio.google.com/api-keys).

If Flask is running, stop it with `Ctrl+C`. Run the prompt for your terminal, then paste your key and press Enter. Enter the real key only in your local terminal.

**Windows Command Prompt (CMD)**

```cmd
set /p "GEMINI_API_KEY=Paste your Gemini API key: "
```

**Windows PowerShell**

```powershell
$env:GEMINI_API_KEY = Read-Host "Paste your Gemini API key"
```

**macOS or Linux (Bash or Zsh)**

```bash
printf 'Paste your Gemini API key: '
IFS= read -r -s GEMINI_API_KEY && export GEMINI_API_KEY && printf '\n'
```

In the same terminal, rerun the `app.py` launch command from the setup above. If you open a new terminal, enter the key again.

1. Choose a JPG, PNG, or WebP image up to 10 MB and select **Analyze photo**. The app sends a resized copy to Google Gemini for ingredient suggestions.
2. Review the suggested pantry rows and enter the amounts you have.
3. Select **Find dinner plan** to update the plan and shopping list.

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

To test photo-assisted entry, load the sample and try a photo of tomatoes and onions. Confirm **3 tomatoes** and **2 onions** in the pantry. Recalculate to see the shopping total drop to **NIS 11.50**.

## How it works

`app.py` validates the form and calls `find_plan`. The planner tries every combination of three starter recipes. For each combination, `price_basket` adds the required quantities, subtracts pantry stock once, and rounds each remaining amount up to a whole pack. Prices are kept as integer agorot, with 100 agorot equal to NIS 1. Flask renders the cheapest basket the planner found within the cap.

| Walkthrough owner | Open these files | Explain or show |
| --- | --- | --- |
| Omar Kadan | `planner/shopping_list.py`, `planner/meal_plan.py` | Explain why pricing all three recipes together matters. Show how tomatoes are pooled and how a budget equal to the basket cost is accepted. |
| Obida Jbara | `app.py`, `templates/`, `static/styles.css` | Trace the budget and ingredients from the browser form into Python, then show where the result and validation messages are rendered. |
| Basil Haj Yahia | `data/`, `planner/catalog.py`, `tests/` | Explain how recipes reference catalog IDs and units. Walk through the hand-calculated basket and run the exact-cap and below-cap checks. |

## Run the checks

Use the virtual environment's Python from above, followed by `-m unittest discover -s tests -v`.

**Windows Command Prompt (CMD)**

```cmd
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Windows PowerShell**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**macOS or Linux**

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

The demo plans meals from starter recipes. AI recipe suggestions are a future feature described in the proposal. The initial demo files were drafted with AI assistance.
