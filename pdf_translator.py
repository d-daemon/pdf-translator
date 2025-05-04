"""Translate PDF files."""

import os
from argparse import Namespace

from colorama import Fore, init

from src.core import (
    detect_language,
    extract_text_from_pdf,
    generate_output_filename,
    options_parser,
    process_output_file,
    translate_text,
)
from src.utils.io import handle_file_path_conflict, normalize_path_input, validate_file_exists
from src.utils.language_map import normalize_language_code
from src.utils.transformation import clean_extracted_text

init(autoreset=True)

def extract_and_process_pdf(pdf_path: str, should_clean: bool = False) -> str | None:
    """Extract text from PDF and optionally clean it.

    Args:
        pdf_path: Path to the PDF file
        should_clean: Whether to clean the extracted text

    Returns:
        Processed text or None if extraction failed

    """
    try:
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(Fore.RED + "Error: No text found in the PDF.")
            return None

        return clean_extracted_text(text) if should_clean else text

    except Exception as e:
        print(Fore.RED + f"Failed to extract or clean text: {e}")
        return None

def get_normalized_languages(src_lang: str | None, tgt_lang: str, text: str) -> tuple[str | None, str]:
    """Get normalized language codes, detecting source language if needed.

    Args:
        src_lang: Source language code or None for auto-detection
        tgt_lang: Target language code
        text: Text to use for language detection if needed

    Returns:
        Tuple of (normalized source language, normalized target language)

    """
    norm_src_lang = normalize_language_code(src_lang) if src_lang else None
    norm_tgt_lang = normalize_language_code(tgt_lang)

    if not norm_src_lang:
        print(Fore.YELLOW + "No source language provided. Detecting...")
        detected = detect_language(text)
        if not detected:
            print(Fore.RED + "Failed to detect source language. Exiting.")
            return None, norm_tgt_lang
        norm_src_lang = normalize_language_code(detected)
        print(Fore.GREEN + f"Detected source language: {norm_src_lang}")

    return norm_src_lang, norm_tgt_lang

def validate_output_format(output_format: str) -> bool:
    """Validate that the output format is supported.

    Args:
        output_format: Output format to validate

    Returns:
        True if the format is supported, False otherwise

    """
    supported_exts = {"txt", "html", "md"}
    if output_format not in supported_exts:
        print(Fore.RED + f"Error: Unsupported output format '{output_format}'. Supported: txt, html, md.")
        return False
    return True

def prompt_for_missing_options(args: Namespace) -> None:
    """Prompt user for missing command line options.

    Args:
        args: Parsed command line arguments

    """
    if not args.pdf_path:
        path_input = input("\nPlease enter the PDF file path: ").strip()
        args.pdf_path = normalize_path_input(path_input)

    if not args.src:
        src_input = input("\nOptional: Enter source language (or leave blank to auto-detect): ").strip()
        args.src = src_input or None

    if not args.tgt:
        tgt_input = input("\nOptional: Enter target language (default: en): ").strip()
        args.tgt = tgt_input or "en"

    if not args.clean:
        use_clean_input = input(
            "\nOptional: Clean text before translation? (leave blank for default: N) (y/N): ").strip().lower()
        args.clean = use_clean_input == "y"

    if not args.ext:
        ext_input = input("\nOptional: Enter output format (txt, html, md). Default: txt: ").strip().lower()
        args.ext = ext_input or "txt"

def main() -> None:
    """Initialize the script and handle command line arguments."""
    parser = options_parser()
    args = parser.parse_args()

    prompt_for_missing_options(args)

    if not validate_file_exists(args.pdf_path, "PDF file"):
        return

    processed_text = extract_and_process_pdf(args.pdf_path, should_clean=args.clean)
    if processed_text is None:
        return

    src_lang, tgt_lang = get_normalized_languages(args.src, args.tgt, processed_text)
    if src_lang is None:
        return

    output_ext = args.ext.lower()
    if not validate_output_format(output_ext):
        return

    try:
        translated_text = translate_text(processed_text, src_lang, tgt_lang)
    except Exception as e:
        print(Fore.RED + f"Translation failed: {e}")
        return

    output_base_path = generate_output_filename(args.pdf_path, src_lang, tgt_lang)
    output_full_path = os.path.splitext(output_base_path)[0] + f".{output_ext}"
    output_full_path = handle_file_path_conflict(output_full_path, args.overwrite)

    try:
        title = f"Translation of {os.path.basename(args.pdf_path)} from {src_lang} to {tgt_lang}"
        process_output_file(output_full_path, translated_text, output_ext, title)
        print(Fore.GREEN + f"\nTranslation from {src_lang} to {tgt_lang} completed. Output saved to: {output_full_path}")
    except Exception as e:
        print(Fore.RED + f"Program failed: {e}")
        return

if __name__ == "__main__":
    main()
