"""Utility functions for output formatting."""

from collections.abc import Callable


def format_as_text(content: str, title: str | None = None) -> str:
    """Format content as plain text.

    Args:
        content: Content to format
        title: Not used in this format

    Returns:
        Formatted text

    """
    return content

def format_as_html(content: str, title: str | None = None) -> str:
    """Format content as HTML.

    Args:
        content: Content to format
        title: Optional title for the HTML document

    Returns:
        Formatted HTML

    """
    title_tag = f"<title>{title}</title>" if title else ""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {title_tag}
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            max-width: 900px;
        }}
        pre {{
            white-space: pre-wrap;
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <pre>{content}</pre>
</body>
</html>"""

def format_as_markdown(content: str, title: str | None = None) -> str:
    """Format content as Markdown.

    Args:
        content: Content to format
        title: Optional title for the Markdown document

    Returns:
        Formatted Markdown

    """
    title_section = f"# {title}\n\n" if title else ""
    return f"{title_section}```\n{content}\n```"

FormatterType = Callable[[str, str | None], str]

def get_formatter(format_type: str) -> FormatterType:
    """Get the appropriate formatter function for the specified format.

    Args:
        format_type: Format type (txt, html, md)

    Returns:
        Formatter function

    """
    formatters: dict[str, FormatterType] = {
        "txt": format_as_text,
        "html": format_as_html,
        "md": format_as_markdown,
    }
    return formatters.get(format_type.lower(), format_as_text)
