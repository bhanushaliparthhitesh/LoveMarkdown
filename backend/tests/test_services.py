from app.services import estimate_tokens, optimize_markdown


def test_optimize_markdown_collapses_extra_whitespace() -> None:
    source = "# Title  \n\n\nParagraph\n\n\n- item\n"
    assert optimize_markdown(source) == "# Title\n\nParagraph\n\n- item\n"


def test_estimate_tokens_empty_text() -> None:
    assert estimate_tokens("") == 0


def test_estimate_tokens_non_empty_text() -> None:
    assert estimate_tokens("one two three") >= 1
