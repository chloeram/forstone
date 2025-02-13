# notes_parser.py

import pdfplumber

def parse_notes(filepath: str) -> list[str]:

    notes = []
    with pdfplumber.open(filepath) as pdf: # Open PDF file
        for page in pdf.pages: # Iterate through each page
            text = page.extract_text() or "" # Extract text from each page

            lines = text.split("\n") # Split text into lines
            for line in lines: # Iterate through each line
                line = line.strip() # Clean

                if line:
                    item = ContentItem(
                        source="note",
                        text=line,
                        metadata={}
                    )
                    notes.append(item)

    return notes