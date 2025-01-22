import os
import pytest
from parsing.transcripts_parser import parse_transcript

def test_parse_pdf_transcript():
    test_pdf_path = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'sample_transcript.pdf'
    )

    parsed_lines = parse_pdf_transcript(test_pdf_path)

    assert len(parsed_lines) > 0, "Parser should return at least one line" # Checks that something is returned

    first_line = parsed_lines[0]
    assert "text" in first_line, "Each entry should have a 'text' key"
    assert "slide_ref" in first_line, "Each entry should have a 'slide_ref' key"
