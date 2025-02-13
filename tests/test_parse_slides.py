import unittest
from src.parsing.slides_parser import parse_pdf_slides, parse_pptx_slides
from src.content_models import ContentItem

class TestParseSlides(unittest.TestCase):
    def test_slides_parsing(self):
        sample_file = 'tests/lecture17_slides.pdf'
        slides = parse_pdf_slides(sample_file)
        
        self.assertIsInstance(slides, list) # Check that non empty list
        self.assertGreater(len(slides), 0)

        """
        print("\n--- Parsed Slides ---")
        for item in slides:
            print(item)
            print("\n\n")
        print("---------------------\n")
        """

        for item in slides:
            self.assertIsInstance(item, ContentItem)
            #self.assertTrue('slide_num' in item.metadata or 'title' in item.metadata)
            self.assertIsInstance(item.text, str)

if __name__ == '__main__':
    unittest.main()