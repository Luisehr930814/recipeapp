#!/usr/bin/env python3
"""
Command‑line tool for suggesting recipes and planning meals.

This script forms the core of the RecipeApp project. It prompts the user for
available ingredients, recommends recipes from a small internal database,
generates shopping lists and helps to plan meals for the week.

It is designed to run in a terminal and uses only the Python standard
library. For more details, see the README.md file in the repository.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Iterable
import sys


@dataclass
class Recipe:
    """Simple representation of a recipe and its required ingredients."""

    name: str
    ingredients: List[str]
    instructions: str = ""

    def missing_ingredients(self, available: Iterable[str]) -> List[str]:
        """Return a list of ingredients required for this recipe that are not available."""
        available_set = {i.lower() for i in available}
        return [ing for ing in self.ingredients if ing.lower() not in available_set]


def load_recipes() -> List[Recipe]:
    """Load a small library of example recipes.

    In a more complete application this function could read recipes from a file
    or database. Here we define a handful of recipes inline.
    """
    return [
        Recipe(
            name="Pasta with Tomato Sauce",
            ingredients=["pasta", "tomato", "garlic", "olive oil", "salt"],
            instructions=textwrap.dedent(
                """
                1. Cook the pasta according to package instructions.
                2. Heat olive oil in a pan and sauté minced garlic until fragrant.
                3. Add chopped tomatoes and simmer until sauce thickens. Season with salt.
                4. Combine the pasta with the sauce and serve warm.
                """
            ).strip(),
        ),
        Recipe(
            name="Omelette",
            ingredients=["eggs", "butter", "cheese", "salt", "pepper"],
            instructions=textwrap.dedent(
                """
                1. Beat the eggs in a bowl and season with salt and pepper.
                2. Melt butter in a non‑stick pan over medium heat.
                3. Pour in the eggs and cook until just set, then sprinkle cheese over half.
                4. Fold the omelette and slide onto a plate.
                """
            ).strip(),
        ),
        Recipe(
            name="Fresh Salad",
            ingredients=["lettuce", "tomato", "cucumber", "olive oil", "lemon", "salt"],
            instructions=textwrap.dedent(
                """
                1. Wash and chop the lettuce, tomato and cucumber.
                2. In a bowl, whisk together olive oil, lemon juice and salt to make a dressing.
                3. Toss the vegetables with the dressing and serve immediately.
                """
            ).strip(),
        ),
        Recipe(
            name="Grilled Cheese Sandwich",
            ingredients=["bread", "cheese", "butter"],
            instructions=textwrap.dedent(
                """
                1. Butter one side of each slice of bread.
                2. Place a slice of cheese between two pieces of bread, buttered sides facing out.
                3. Grill in a pan over medium heat until both sides are golden and the cheese is melted.
                """
            ).strip(),
        ),
    ]


def suggest_recipes(recipes: List[Recipe], available: List[str]) -> List[Tuple[Recipe, List[str]]]:
    """Return a list of (recipe, missing_ingredients) tuples sorted by how many ingredients are missing.

    Recipes that can be made entirely with available ingredients will appear first.
    """
    suggestions = []
    for recipe in recipes:
        missing = recipe.missing_ingredients(available)
        suggestions.append((recipe, missing))
    # Sort by number of missing ingredients ascending
    suggestions.sort(key=lambda x: len(x[1]))
    return suggestions


def print_suggestions(suggestions: List[Tuple[Recipe, List[str]]]) -> None:
    """Print recipe suggestions to the console in a user‑friendly way."""
    print("\nRecipe Suggestions:")
    for idx, (recipe, missing) in enumerate(suggestions, start=1):
        status = "Ready to cook" if not missing else f"Missing {len(missing)}"
        print(f" {idx}. {recipe.name} – {status}")
    print()


def choose_recipes(suggestions: List[Tuple[Recipe, List[str]]]) -> List[Recipe]:
    """Prompt the user to choose recipes by number. Returns the selected Recipe objects."""
    indices: List[int] = []
    try:
        selection = input("Enter the numbers of the recipes you want to cook (comma separated), or press Enter to skip: ")
    except EOFError:
        # In case of non‑interactive environment
        return []
    if not selection.strip():
        return []
    parts = [p.strip() for p in selection.split(',') if p.strip()]
    for part in parts:
        try:
            idx = int(part)
            if 1 <= idx <= len(suggestions):
                indices.append(idx - 1)
            else:
                print(f"Ignoring invalid recipe number: {idx}")
        except ValueError:
            print(f"Ignoring invalid input: {part}")
    # Deduplicate while preserving order
    seen: set[str] = set()
    chosen: List[Recipe] = []
    for idx in indices:
        recipe = suggestions[idx][0]
        if recipe.name not in seen:
            chosen.append(recipe)
            seen.add(recipe.name)
    return chosen


def generate_shopping_list(recipe: Recipe, available: List[str]) -> List[str]:
    """Return a list of ingredients you need to buy for the given recipe."""
    return recipe.missing_ingredients(available)


def create_meal_plan(recipes: List[Recipe], days: int = 7) -> Dict[str, Recipe]:
    """Create a simple weekly meal plan given a list of recipes.

    The plan will cycle through the provided recipes. If there are fewer recipes
    than days, they will repeat in order.
    """
    day_names = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ][:days]
    plan: Dict[str, Recipe] = {}
    for i, day in enumerate(day_names):
        recipe = recipes[i % len(recipes)]
        plan[day] = recipe
    return plan


def main() -> None:
    print(textwrap.dedent(
        """
        ========================================
        Welcome to RecipeApp! 🎉

        This tool helps you decide what to cook based on the ingredients you
        have on hand, and generates shopping lists and meal plans.
        ========================================
        """
    ))

    # Prompt for available ingredients
    try:
        raw = input("Enter the ingredients you have (comma separated): ")
    except EOFError:
        # Provide default list if run in a non‑interactive environment
        raw = ""
    available = [item.strip().lower() for item in raw.split(',') if item.strip()]

    recipes = load_recipes()
    suggestions = suggest_recipes(recipes, available)
    print_suggestions(suggestions)

    # Let user pick recipes for shopping list and meal plan
    chosen = choose_recipes(suggestions)
    if chosen:
        # For each chosen recipe, print missing ingredients
        for recipe in chosen:
            missing = generate_shopping_list(recipe, available)
            print(f"\nShopping list for {recipe.name}:")
            if missing:
                for ing in missing:
                    print(f" - {ing}")
            else:
                print("You have everything you need!")
    else:
        print("No recipes selected.")

    # Ask if user wants a weekly meal plan
    if chosen:
        try:
            answer = input("\nWould you like to generate a weekly meal plan from these recipes? (y/n): ")
        except EOFError:
            answer = "n"
        if answer.strip().lower().startswith('y'):
            plan = create_meal_plan(chosen, days=7)
            print("\nYour meal plan for the week:")
            for day, recipe in plan.items():
                print(f" {day}: {recipe.name}")
        else:
            print("Meal plan skipped.")
    print("\nThank you for using RecipeApp!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting RecipeApp. Goodbye!")
        sys.exit(0)