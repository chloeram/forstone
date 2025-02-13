import unittest
from src.parsing.transcript_parser import parse_transcript  # adjust the import as needed
from src.content_models import ContentItem

class TestParseTranscript(unittest.TestCase):
    def test_transcript_parsing(self):
        sample_file = 'tests/lecture17_transcript.pdf'
        transcript = parse_transcript(sample_file)
        
        self.assertIsInstance(transcript, list)
        self.assertGreater(len(transcript), 0)
        
        print("\n--- Parsed Transcript ---")
        for item in transcript:
            print(item)
            print("\n\n")
        print("---------------------\n")

        for item in transcript:
            self.assertIsInstance(item, ContentItem)
            #self.assertIn('timestamp', item.metadata)
            self.assertIsInstance(item.text, str)

if __name__ == '__main__':
    unittest.main()