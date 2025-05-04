# PDF Translator Tool

Simple CLI tool to extract, optionally clean, translate, and save the contents of a PDF file.  
Powered by `deep_translator`, `PyMuPDF`, `langdetect`, and designed for general-purpose document translation.

---

## Features

- 🗂️ Extract text from PDF files
- 🌎 Auto-detect source language
- 🔄 Translate to any supported language
- 🧹 Optional text cleaning (fix line breaks, spaced letters)
- 📄 Save output as `.txt`, `.html`, or `.md` file formats
- 🔥 Supports overwrite prompts to avoid accidental file loss

---

## Installation

- Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- Or use your Python environment manager like uv.

  ```bash
  uv pip install -r requirements.txt
  ```

---

## Usage

- Basic command using `python` interpreter:

  ```bash
  python pdf_translator.py /path/to/your/inputfile.pdf
  ```

- Basic command using `uv` interpreter:

  ```bash
  uv run pdf_translator.py /path/to/your/inputfile.pdf
  ```

---

## CLI Options

| Flag                        | Description | Expected Input | Default Behavior |
|:----------------------------|:---|:---|:---|
| `-s`, `--src`, `--src_lang` | Source language code | ISO 639-1 language code (e.g., `de`, `fr`) | Auto-detect if not provided |
| `-t`, `--tgt`, `--tgt_lang` | Target language code | ISO 639-1 language code | `en` (English) |
| `-c`, `--clean`               | Apply cleaning (fix broken spacing) | Boolean flag (`-c` to enable) | Disabled (raw text used by default) |
| `-f`, `--overwrite`         | Overwrite output file if it already exists | Boolean flag (`-f` to enable) | Prompts user if file exists |
| `-e`, `--ext`               | Output file format | `txt`, `html`, `md` | `txt` |
| `pdf_path`                  | Path to the input PDF file | String (file path) | Required if not provided in prompt |

---

## Example Commands

- Translate from German to English, save as default `.txt` output file type:

  ```bash
  uv run pdf_translator.py --src_lang de --tgt_lang en /path/to/file.pdf
  ```

- Translate and save output as HTML:

  ```bash
  uv run pdf_translator.py --src de --tgt en --ext html /path/to/file.pdf
  ```

- Auto-detect language, apply cleaning to raw text, save as Markdown:

  ```bash
  uv run pdf_translator.py -c -e md /path/to/file.pdf
  ```

- Full options (Chinese to English, clean raw text, force override output, save as txt)

  ```bash
  uv run pdf_translator.py -s zh-CN -t en -c -f -e txt /path/to/file.pdf

---

## Output

- Output file will be saved in the same folder as the source PDF.
- Filename format:

  ```python
  original_filename_{source_language}_{target_language}.{extension}
  ```

- Example:

  ```bash
  Input file: /Users/test/sample.pdf
  Output file: /Users/test/sample_de_en.txt
  ```

---

## Notes

- Text cleaning removes unwanted line breaks and fixes spaced letters.
- Only `.txt`, `.html`, and `.md` are supported currently.
- Future enhancements may include support for `.pdf`, `.docx`, `.rtf` output.

---

## License

This project is licensed under the [MIT License](https://github.com/d-daemon/pdf-translator/blob/main/LICENSE).
