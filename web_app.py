#!/usr/bin/env python3
""" Simple Flask web interface for the RecipeApp. This
module exposes a minimal web application that lets users input the ingredients
they have on hand and returns a list of recipes they can cook along with any
missing ingredients. It reuses the core logic from the command-line tool.
To run the server locally, install Flask (`pip install flask`) and then execute this
script. Visit http://localhost:5000 in your browser. """

from __future__ import annotations

import os
from flask import Flask, request, render_template_string
from recipe_app import load_recipes, suggest_recipes
from vision import scan_ocr, normalize_ingredients
from PIL import Image

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>RecipeApp</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        .container { max-width: 600px; margin: auto; }
        input[type=text], textarea { width: 100%; padding: 8px; margin: 8px 0; box-sizing: border-box; }
        button { padding: 10px 20px; font-size: 1rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h1>RecipeApp</h1>
        <p>Enter the ingredients you have (comma separated) to see which recipes you can make.</p>
        <form method="post" action="/" enctype="multipart/form-data">
            <label for="ingredients">Ingredients:</label>
            <input type="text" id="ingredients" name="ingredients" required>
            <button type="submit">Find Recipes</button>
        </form>
        <hr>
        <h2>Or upload a photo of ingredient list</h2>
        <form method="post" action="/scan" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Scan Ingredients</button>
        </form>
        {% if suggestions %}
        <h2>Suggested Recipes</h2>
        <table>
            <thead><tr><th>Recipe</th><th>Missing Ingredients</th></tr></thead>
            <tbody>
            {% for name, missing in suggestions %}
                <tr><td>{{ name }}</td><td>{{ ', '.join(missing) if missing else 'None' }}</td></tr>
            {% endfor %}
            </tbody>
        </table>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        raw = request.form.get("ingredients", "")
        ingredients = normalize_ingredients(raw)
        recipes = load_recipes()
        suggestions = suggest_recipes(ingredients, recipes)
        return render_template_string(INDEX_HTML, suggestions=suggestions)
    # GET request
    return render_template_string(INDEX_HTML, suggestions=None)

@app.route("/scan", methods=["POST"])
def scan():
    # handle image upload and OCR
    file = request.files.get("image")
    if not file:
        return render_template_string(INDEX_HTML, suggestions=[])
    image = Image.open(file.stream)
    text = scan_ocr(image)
    ingredients = normalize_ingredients(text)
    recipes = load_recipes()
    suggestions = suggest_recipes(ingredients, recipes)
    return render_template_string(INDEX_HTML, suggestions=suggestions)
