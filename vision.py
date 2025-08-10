#!/usr/bin/env python3
"""
Utility functions for image-based ingredient recognition using OCR.

This module uses the pytesseract library to extract text from images and
provides helper functions to normalise that text into a list of ingredient names.
"""

from __future__ import annotations

import pytesseract
from PIL import Image
import re
import unicodedata
from typing import List

# Synonym mapping from Spanish or alternative words to canonical ingredient names used in recipes.json
INGREDIENT_SYNONYMS = {
    'harina': 'flour',
    'huevo': 'egg',
    'huevos': 'egg',
    'leche': 'milk',
    'azucar': 'sugar',
    'aceite': 'oil',
    'sal': 'salt',
    'queso': 'cheese',
    'tomate': 'tomato',
    'tomates': 'tomato',
    'cebolla': 'onion',
    'ajo': 'garlic',
    'pimienta': 'pepper',
    'mantequilla': 'butter',
    'manteca': 'butter',
    'pollo': 'chicken',
    'carne': 'beef',
    'res': 'beef',
    'yogur': 'yogurt',
    'yogurt': 'yogurt',
    'fresa': 'strawberries',
    'fresas': 'strawberries',
    'platano': 'banana',
    'platanos': 'banana'
    # add more synonyms as needed
}

def scan_ocr(image: Image.Image) -> str:
    """
    Use Tesseract OCR to extract raw text from an uploaded image.

    Args:
        image: A Pillow Image instance.

    Returns:
        The raw text recognized by the OCR engine.
    """
    return pytesseract.image_to_string(image)


def normalize_ingredients(text: str) -> List[str]:
    """
    Normalize raw OCR text into a list of ingredient names.

    This function lowercases the text, strips accents, splits into tokens
    and replaces known synonyms.

    Args:
        text: Raw OCR text.

    Returns:
        A list of ingredient names.
    """
    # Remove accents
    text_norm = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # Split into words by non-alphanumeric characters
    tokens = re.split(r'[^a-zA-Z0-9]+', text_norm.lower())
    ingredients: List[str] = []
    for token in tokens:
        if not token:
            continue
        # Map synonyms to canonical names
        canonical = INGREDIENT_SYNONYMS.get(token, token)
        ingredients.append(canonical)
    return ingredients

__all__ = ['scan_ocr', 'normalize_ingredients']
