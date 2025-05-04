"""Content transformation functions."""

import re


def fix_single_letter_spacing(text: str) -> str:
    """Fix excessive spacing between letters in words."""
    return re.sub(r"\b(?:[A-ZÄÖÜa-zäöü]-?\s){2,}[A-ZÄÖÜa-zäöü]\b",
                  lambda m: m.group(0).replace(" ", "").replace("- ", "-"),
                  text)

def fix_hyphen_linebreaks(text: str) -> str:
    """Merge words split across lines with hyphens."""
    return re.sub(r"-\s*\n\s*", "", text)

def clean_extracted_text(text: str) -> str:
    """Cleanse extracted text by removing unwanted characters and spacing."""
    text = fix_hyphen_linebreaks(text)
    text = fix_single_letter_spacing(text)
    return text
