#!/usr/bin/env python3
"""
Simple Flask web interface for the RecipeApp.

This module exposes a minimal web application that lets users input the
ingredients they have on hand and returns a list of recipes they can cook
along with any missing ingredients. It reuses the core logic from the
command‑line tool.

To run the server locally, install Flask (``pip install flask``) and then
execute this script. Visit http://localhost:5000 in your browser.
"""

from __future__ import annotations

import os
from flask import Flask, request, render_template_string
from recipe_app import load_recipes, suggest_recipes

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
      <form action="/suggest" method="post">
        <input type="text" name="ingredients" placeholder="e.g. pasta, tomato, cheese" required>
        <button type="submit">Get Suggestions</button>
      </form>
      {% if suggestions %}
      <h2>Suggestions</h2>
      <table>
        <tr><th>Recipe</th><th>Status</th><th>Missing Ingredients</th></tr>
        {% for recipe, missing in suggestions %}
          <tr>
            <td>{{ recipe.name }}</td>
            <td>{{ 'Ready' if not missing else 'Missing ' + missing|length|string }}</td>
            <td>{{ ', '.join(missing) if missing else '—' }}</td>
          </tr>
        {% endfor %}
      </table>
      {% endif %}
    </div>
  </body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    return render_template_string(INDEX_HTML, suggestions=None)


@app.route('/suggest', methods=['POST'])
def suggest():
    raw = request.form.get('ingredients', '')
    ingredients = [x.strip().lower() for x in raw.split(',') if x.strip()]
    recipes = load_recipes()
    suggestions = suggest_recipes(recipes, ingredients)
    return render_template_string(INDEX_HTML, suggestions=suggestions)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)