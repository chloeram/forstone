# transcript_parser.py

import re
import pdfplumber
import spacy
from src.content_models import ContentItem

# Load spaCy model 
nlp = spacy.load("en_core_web_sm")

# Regex to detect any timestamps
TIMESTAMP_REGEX = re.compile(r'(\d{1,2}:\d{2}(?::\d{2})?)')

# Regex to detect any referenced slide numbers
SLIDENUM_REGEX = re.compile(r"slide\s*#?(\d+)", re.IGNORECASE)

"""
parse_transcript() parses inputted transcript into chunks of sentences to preserve context
"""
def parse_transcript(filepath: str) -> list[dict]:
    transcript = []

    with pdfplumber.open(filepath) as pdf: # Open PDF file
        for page in pdf.pages: # Iterate through pages in PDF

            # Extract text from each page if any, else None
            page_text = page.extract_text() or "" 
            if not page_text.strip():
                continue

            # Using spaCy to segment text into sentences
            doc = nlp(page_text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

            # Merge sentences into chunks to preserve context
            merged_chunks = []
            current_chunk = ""
            min_length = 700 # TODO - test and change

            for sentence in sentences:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

                # If the current chunk is long enough and ends with a strong punctuation mark, end it
                if len(current_chunk) >= min_length and current_chunk[-1] in ".?!":
                    merged_chunks.append(current_chunk)
                    current_chunk = ""

            # Add remaining text as a final chunk
            if current_chunk:
                merged_chunks.append(current_chunk)

            # Process each merged chunk to create ContentItem objects
            for chunk in merged_chunks:
                # Extract timestamp if any, else None
                timestamp_match = TIMESTAMP_REGEX.search(chunk)
                timestamp = timestamp_match.group(1) if timestamp_match else None
    
                # Extract slide ref if any, else None
                slide_match = SLIDENUM_REGEX.search(chunk)
                slide_num = slide_match.group(1) if slide_match else None

                # Create metadata dictionary
                metadata = {}
                if timestamp:
                    metadata["timestamp"] = timestamp
                if slide_num:
                    metadata["slide_num"] = slide_num

                # Create ContentItem
                item = ContentItem(
                    source="transcript",
                    text=chunk,
                    metadata=metadata
                )

                transcript.append(item)

    # Return list of dictionaries
    return transcript

