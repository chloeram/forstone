import pdfplumber
import pptx
from sentence_transformers import SentenceTransformer
from PIL import Image
import spacy

def main():
    print("All libraries are installed and working!")

    # Loading a model to verify
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Sentence Transformer loaded successfully.")

if __name__ == "__main__":
    main()
