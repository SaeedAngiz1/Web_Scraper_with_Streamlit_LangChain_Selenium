import pytest
from scrape import clean_body_content

def test_clean_body_content_removes_script_and_style():
    html_content = """
    <html>
        <body>
            <h1>Hello World</h1>
            <script>console.log('test');</script>
            <style>body { color: red; }</style>
            <p>This is a paragraph.</p>
        </body>
    </html>
    """
    cleaned = clean_body_content(html_content)
    assert "console.log" not in cleaned
    assert "body { color: red; }" not in cleaned
    assert "Hello World" in cleaned
    assert "This is a paragraph." in cleaned

    # Check exact output
    lines = cleaned.splitlines()
    assert lines == ["Hello World", "This is a paragraph."]

def test_clean_body_content_strips_whitespaces():
    html_content = """
    <body>

        <div>
            Text with
        </div>

        <p>
            spaces
        </p>
    </body>
    """
    cleaned = clean_body_content(html_content)
    assert cleaned == "Text with\nspaces"

def test_clean_body_content_empty_input():
    assert clean_body_content("") == ""

def test_clean_body_content_no_script_or_style():
    html_content = "<p>Just a simple paragraph.</p>"
    assert clean_body_content(html_content) == "Just a simple paragraph."
