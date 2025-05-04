"""Core functionality for PDF translation."""

import argparse
import os
from typing import Optional

import pymupdf
from colorama import Fore
from deep_translator import GoogleTranslator
from langdetect import detect

from src.utils.formatting import get_formatter
from src.utils.io import ensure_directory_exists


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text from the PDF

    """
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def detect_language(text: str) -> str | None:
    """Auto-detect language if source language is not specified.

    Args:
        text: Text to detect language from

    Returns:
        Detected language code or None if detection fails

    """
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        print(Fore.RED + f"Language detection failed: {e}")
        return None

def translate_text(text: str, src_lang: str, tgt_lang: str) -> str:
    """Translate text using Google Translator.

    Args:
        text: Text to translate
        src_lang: Source language code
        tgt_lang: Target language code

    Returns:
        Translated text

    """
    translator = GoogleTranslator(source=src_lang, target=tgt_lang)
    return translator.translate(text)

def generate_output_filename(original_filename: str, src_lang: str, tgt_lang: str) -> str:
    """Generate output filename in the same directory as source PDF.

    Args:
        original_filename: Original PDF file path
        src_lang: Source language code
        tgt_lang: Target language code

    Returns:
        Generated output filename path

    """
    base_dir = os.path.dirname(original_filename)
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    output_name = f"{base_name}_{src_lang}_{tgt_lang}"
    return os.path.join(base_dir, output_name)

def options_parser() -> argparse.ArgumentParser:
    """Parse command line arguments.

    Returns:
        ArgumentParser object with all arguments configured

    """
    parser = argparse.ArgumentParser(description="Translate a PDF file.")
    parser.add_argument("-s", "--src", "--src_lang", type=str, help="Source language code (optional)")
    parser.add_argument("-t", "--tgt", "--tgt_lang", type=str, default="en", help="Target language code (default: en)")
    parser.add_argument("-f", "--overwrite", action="store_true", help="Overwrite existing files if output exists")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean text before translation")
    parser.add_argument("-e", "--ext", type=str, default="txt",
                        help="Desired output file format (txt, html, md). Default: txt")
    parser.add_argument("pdf_path", type=str, nargs="?", help="Path to the input PDF file (optional)")
    return parser

def process_output_file(output_path: str, translated_text: str, output_format: str, title: Optional[str] = None) -> None:
    """Process and save translated output to file in the specified format.

    Args:
        output_path: Path to save the output file
        translated_text: Translated text to save
        output_format: Format to save the output as (txt, html, md)
        title: Optional title for formatted output

    """
    try:
        formatter = get_formatter(output_format)
        formatted_text = formatter(translated_text, title)

        ensure_directory_exists(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted_text)
    except Exception as e:
        print(Fore.RED + f"Failed to save the output file: {e}")
        raise
