# RecipeApp

RecipeApp is a small command‑line and web tool that demonstrates the core features of the food‑scanner project we’ve been developing. The goal of the project is to make it easier to cook at home by recognising which ingredients you have on hand, suggesting recipes that use those ingredients and helping you plan your shopping list and weekly meals.

## Features

* **Ingredient input** – For now there is no image recognition component. Instead, the tool prompts you to enter the ingredients you have available, simulating the recognition step.
* **Web interface** – A lightweight Flask web app (`web_app.py`) provides a simple HTML form to enter your ingredients and view recipe suggestions in your browser.
* **Recipe suggestions** – The app compares your available ingredients against a small library of recipes and recommends dishes you can make. Each recipe lists the ingredients required.
* **Shopping list generation** – Once you select a recipe, the tool identifies which ingredients you still need and presents a shopping list.
* **Meal planning** – When you pick multiple recipes, the app can create a simple meal plan for the week, assigning one recipe per day.

## Usage

1. Install the dependencies (if any) listed in `requirements.txt` using `pip install -r requirements.txt`. This script only depends on Python’s standard library, so no external packages are required.
2. Run the script:

```sh
python recipe_app.py
```

3. Follow the on‑screen prompts to enter your available ingredients and select recipes. The program will display suggestions, missing ingredients and an optional weekly meal plan.

### Running the web app

To try the web interface instead of the command line, install Flask (`pip install flask`) and then run:

```sh
python web_app.py
```

Open `http://localhost:5000` in your browser, enter your ingredients and view the recipe suggestions. The web app currently supports manual text input for ingredients; file uploads for image scanning are not yet implemented.

## Extending the project

This version is intentionally simple. To turn it into a fully fledged application you could:

* Replace the manual ingredient input with real image recognition using an OCR or object detection library, such as [`pytesseract`](https://github.com/madmaze/pytesseract) or [TensorFlow](https://www.tensorflow.org/). This would allow the app to scan a photo of your pantry and extract ingredient names.
* Connect the Flask web app to the image‑recognition functionality so users can upload photos of their ingredients directly from the browser.
* Expand the recipe database. At the moment the script contains a handful of example recipes; you could load recipes from a database or an API.
  * The repository now includes a `recipes.json` file with additional sample recipes. You can modify or extend this file to add more dishes.
* Build a web or mobile interface. Using a framework like Flask or FastAPI (for web) or React Native (for mobile) would let you package this functionality into an easy‑to‑use user interface.

## License

This project is provided under the MIT license (see `LICENSE`). Feel free to use, modify and share it as you like.