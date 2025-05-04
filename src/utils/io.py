"""Utility functions for file I/O operations."""

import os

from colorama import Fore


def ensure_directory_exists(output_path: str | None) -> None:
    """Create directory if not exists.

    Args:
        output_path: Path to ensure directory exists for

    """
    if output_path:
        output_dir = os.path.dirname(output_path) if os.path.isfile(output_path) or output_path.endswith((".txt", ".html", ".md")) else output_path
    else:
        output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

def normalize_path_input(path_input: str) -> str:
    """Strip surrounding quotes if pasted path has them.

    Args:
        path_input: User-provided file path

    Returns:
        Normalized file path

    """
    return path_input.strip().strip('"').strip("'")

def validate_file_exists(file_path: str, file_type: str = "File") -> bool:
    """Validate that a file exists.

    Args:
        file_path: Path to the file
        file_type: Type of file for error message

    Returns:
        True if the file exists, False otherwise

    """
    if not os.path.exists(file_path):
        print(Fore.RED + f"Error: {file_type} {file_path} does not exist.")
        return False
    return True

def handle_file_path_conflict(output_path: str, overwrite: bool = False) -> str:
    """Handle conflict when output file already exists.

    Args:
        output_path: Original output path
        overwrite: Whether to overwrite existing file

    Returns:
        Final output path to use

    """
    if not os.path.exists(output_path) or overwrite:
        return output_path

    overwrite_choice = input(
        f"\nOutput file already exists:\n{output_path}\n\nOverwrite it? [y/N]: ").strip().lower()
    if overwrite_choice == "y":
        return output_path

    base, ext = os.path.splitext(output_path)
    counter = 1
    new_output_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_output_path):
        counter += 1
        new_output_path = f"{base}_{counter}{ext}"

    print(Fore.YELLOW + f"\nSaving to new file: {new_output_path}")
    return new_output_path

def write_to_file(output_path: str, content: str, mode: str = "w", encoding: str = "utf-8") -> bool:
    """Write content to a file with error handling.

    Args:
        output_path: Path to the output file
        content: Content to write
        mode: File open mode
        encoding: File encoding

    Returns:
        True if write was successful, False otherwise

    """
    try:
        ensure_directory_exists(output_path)
        with open(output_path, mode, encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(Fore.RED + f"Failed to write to file: {e}")
        return False
