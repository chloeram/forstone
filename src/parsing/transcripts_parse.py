import re
import pdfplumber

# Regex pattern to recognize when a certain slide number is mentioned
# - \s* allows spaces (e.g. "slide    3")
# - #? makes the '#' optional
# - (\d+) captures the slide number
SLIDE_NUM_PATTERN = re.compile(r"slide\s*#?(\d+)", re.IGNORECASE)

"""
    Parses PDF transcripts, detects where a slide number is detected.
    Returns a list of dicts like follows:
        "text": line in transcript
        "slide_num": if slide # is detected, else none

"""
def parse_transcripts(filepath: str) -> list[dict]:
    
    transcript_content = []

    with pdfplumber.open(filepath) as pdf: # Open using pdfplumber
        for page in pdf.pages: 
            raw = page.extract_text() or "" # Extracting text from each page
            lines = raw_text.split("\n") # Split text into lines

            for line in lines:
                line = line.strip()
                if not line:
                    continue # Skip empty lines

                match = SLIDE_NUM_PATTERN.search(line) # Check is a slide number is referenced
                if match:
                    slide_number = match.group(1) # Extract the slide number as a string
                    transcript_content.append({
                        "text": line,
                        "slide_number": slide_num
                    })
                else:
                    transcript.append({
                        "text": line,
                        "slide_ref": None
                    })

    return transcript
