# RecipeApp

RecipeApp is a small command-line and web tool that demonstrates the core features of the food scanner project we’ve been developing. The goal of the project is to make it easier to cook at home by recognising which ingredients you have on hand, suggesting recipes that use those ingredients and helping you plan your shopping list and weekly meals.

## Features

- **Ingredient input via form or scan** – You can either type the ingredients you have available or upload a photo of an ingredient list. The photo is processed using a local OCR engine (Tesseract via `pytesseract`) to extract the text, and the app normalises the words to match recipe ingredients.
- **Web interface** – A lightweight Flask web app (`web_app.py`) provides HTML forms to enter your ingredients manually or upload a picture for scanning. The server then displays recipe suggestions in your browser.
- **Recipe suggestions** – The app compares your available ingredients against a small library of recipes and recommends dishes you can make. Each recipe lists the required ingredients.
- **Shopping list generation** – Once you select a recipe, the tool identifies which ingredients you still need and presents a shopping list.
- **Meal planning** – When you pick multiple recipes, the app can create a simple meal plan for the week, assigning one recipe per day.

## Installation

1. Install Python dependencies with pip:

```sh
pip install -r requirements.txt
```

The `requirements.txt` now includes Flask, Pillow and pytesseract for the web interface and OCR support.

2. Install Tesseract OCR on your system (only required for scanning photos):

- **Ubuntu/Debian** – Use your package manager to install the engine and development headers:

  ```sh
  sudo apt install tesseract-ocr
  sudo apt install libtesseract-dev
  ```
  These commands install Tesseract and its developer tools【200365460073750†L56-L62】.

- **macOS** – Install via Homebrew or MacPorts:

  ```sh
  brew install tesseract
  ```
  or
  ```sh
  sudo port install tesseract
  ```
  according to the Tesseract documentation【200365460073750†L148-L173】.

- **Windows** – Download the prebuilt installer (e.g., `tesseract‑ocr‑w64‑setup‑5.x.exe`) from the UB Mannheim repository【448535564386824†L342-L364】. Run the installer, accept the defaults and note the installation directory. After installation, add the installation path (e.g., `C:\Program Files\Tesseract‑OCR`) to your `PATH` environment variable【448535564386824†L448-L516】 so that the `tesseract` command is available system‑wide. You can verify the installation by opening a command prompt and running `tesseract --version`【448535564386824†L521-L526】.

3. (Optional) If the `tesseract` binary is not on your PATH, set the path explicitly in Python by assigning `pytesseract.pytesseract.tesseract_cmd` to the full executable path (for example, `r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'` on Windows).

## Usage

For command‑line use:

1. Run the CLI script:

```sh
python recipe_app.py
```

2. Follow the prompts to enter the ingredients you have available, then view suggested recipes and shopping lists.

For the web interface with scanning support:

1. Ensure all dependencies are installed and Tesseract is available.
2. Start the web server:

```sh
python web_app.py
```

3. Open the provided URL in your browser (typically http://127.0.0.1:5000/). Enter ingredients manually or upload an image of an ingredient list using the “Scan ingredient list” form to see recipe suggestions based on OCR.

## Extending the Project

This project is designed to be easy to extend. Some possible directions include:

- Improving the OCR normalisation and adding language‑specific synonym dictionaries.
- Expanding the recipe database with more diverse cuisine types and detailed instructions.
- Adding a nutrition API to calculate nutritional information for recipes.
- Building a more sophisticated meal planning algorithm that considers dietary requirements, portion sizes, and variety.

Pull requests are welcome!

## License

This project is licensed under the MIT License—see the LICENSE file for details.
