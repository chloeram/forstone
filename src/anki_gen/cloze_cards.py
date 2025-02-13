import genanki
from typing import List
from src.content_models import ContentGroup
import os
import spacy

OUTPUT_DIR = "anki_gen"
os.makedirs(OUTPUT_DIR, exist_ok=True)
nlp = spacy.load("en_core_web_sm")

def extract_key_terms(summary: str) -> List[str]:
    """
    Extracts key terms from a given summary using spaCy.
    Returns a list of key terms suitable for cloze deletions.
    """
    doc = nlp(summary)
    key_terms = list({chunk.text for chunk in doc.noun_chunks})  # Extract unique noun phrases
    return sorted(key_terms, key=lambda x: len(x), reverse=True)  # Sort by length to avoid nesting issues

def create_cloze_deletion(summary: str) -> str:
    """
    Converts key terms into cloze deletions within the summary.
    Uses multiple cloze numbers (`c1`, `c2`, etc.).
    """
    key_terms = extract_key_terms(summary)
    cloze_text = summary
    for i, term in enumerate(key_terms[:5]):  # Limit to 5 deletions to prevent overcomplication
        cloze_text = cloze_text.replace(term, f"{{{{c{i+1}::{term}}}}}")  # Wrap term in cloze deletion format
    return cloze_text

def generate_cloze_cards(groups: List[ContentGroup], deck_name="Lecture Anki Deck") -> str:
    """
    Generates a downloadable Anki deck with cloze deletion flashcards
    based on grouped ContentGroup summaries.
    """
    # Define a valid Cloze Model
    cloze_model = genanki.Model(
        1607392319,  # Unique model ID
        "Cloze Model",
        fields=[
            {"name": "Text"},
            {"name": "References"},
        ],
        templates=[
            {
                "name": "Cloze Card",
                "qfmt": "{{cloze:Text}}",  # Cloze deletion format
                "afmt": "{{cloze:Text}}<br><br><b>References:</b> {{References}}",
            },
        ],
        css="""
        .card {
            font-family: Arial;
            font-size: 20px;
            text-align: left;
            color: black;
            background-color: white;
        }
        .cloze {
            font-weight: bold;
            color: blue;
        }
        """,
    )

    deck = genanki.Deck(2059400110, deck_name)
    notes = []

    for group in groups:
        if not group.summary.strip():
            continue  # Skip empty summaries

        # Create cloze deletions in the summary
        cloze_text = create_cloze_deletion(group.summary)

        # Format references nicely
        references_text = ", ".join(group.references) if group.references else "No references available"

        # Create an Anki note
        note = genanki.Note(
            model=cloze_model,
            fields=[cloze_text, references_text],
            tags=["lecture", "generated"],
        )
        notes.append(note)

    # Add notes to the deck
    for note in notes:
        deck.add_note(note)

    # Define deck output path
    deck_path = os.path.join(OUTPUT_DIR, "lecture_deck.apkg")

    # Save deck
    genanki.Package(deck).write_to_file(deck_path)
    print(f"✅ Anki deck saved at: {deck_path}!")

    return deck_path  # Return path for further processing
