# main.py
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from src.parsing.slides_parser import parse_pdf_slides
from src.parsing.transcript_parser import parse_transcript
from src.processing.process import align
from src.anki_gen.cloze_cards import generate_cloze_cards

def main():
    slides_file = 'tests/lecture15_slides.pdf'
    transcript_file = 'tests/lecture15_transcript.pdf'

    slides_items = parse_pdf_slides(slides_file)
    transcript_items = parse_transcript(transcript_file)

    print("Number of slides items:", len(slides_items))
    print("Number of transcript items:", len(transcript_items))

    # Combine extracted data from all sources
    content_items = slides_items + transcript_items
    
    print("Total content items:", len(content_items))

    # Process the data
    groups = align(content_items, min_cluster_size=2, min_samples=1)

    print("Number of groups formed:", len(groups))

    """
    for idx, group in enumerate(groups):
        print(f"Group {idx+1}:")
        print("Summary:", group.summary)
        print("Number of Content Items:", len(group.matching_items))
        print("References:", group.references)
        print("-" * 50)
    """
    if len(groups) >= 3:
        print("Content items in Group 3:")
        for item in groups[2].matching_items:
            print(f"Source: {item.source} | Text: {item.text} | Metadata: {item.metadata}\n\n")
    else:
        print("Group 3 does not exist.")
    # 
    # Print results to test
    # print(groups[0])

    generate_cloze_cards(groups)

if __name__ == "__main__":
    main()

