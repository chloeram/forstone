# process.py

from sentence_transformers import SentenceTransformer, util
from typing import List
from src.content_models import ContentItem, ContentGroup
import numpy as np
import skfuzzy as fuzz
import hdbscan
import spacy
from transformers import pipeline

# Load NLP model for summarization
nlp = spacy.load("en_core_web_sm")
# Initialize summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_tokens_and_concepts(text: str) -> (List[str], List[str]):
    doc = nlp(text)
    # Extract tokens
    tokens = [token.text for token in doc]
    # Use noun chunks as key concept proxies
    key_concepts = list({chunk.text for chunk in doc.noun_chunks})
    return tokens, key_concepts

def process_content_item(item: ContentItem) -> ContentItem:
    tokens, key_concepts = extract_tokens_and_concepts(item.text)
    # Store tokens and key concepts within the item.
    item.tokens = tokens
    item.key_concepts = key_concepts
    return item

def generate_summary(texts: List[str], key_concepts: List[str] = None) -> str:
    if not texts:
        return "No summary available."
    
    # Combine texts into string
    combined_text = " ".join(texts)
    
    # Create context string to highlight key concepts
    key_context = "Key concepts: " + ", ".join(key_concepts) + ". "
    
    prompt = key_context + combined_text
    
    # Generate summary using the summarizer
    summary = summarizer(prompt, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
    return summary


"""
    align() groups ContentItem objects based on semantic similarity to align the content from various sources

    parameters:
        items: list of ContentItem objects
        similarity threshold: minimum cosine similarity to group items

    returns: list of ContentGroup objects

"""
def align(items: List[ContentItem], min_cluster_size: int = 2, min_samples: int = 1) -> List[ContentGroup]:

    if not items:
        return []

    # Process each ContentItem to extract tokens and key concepts.
    items = [process_content_item(item) for item in items]
    
    # Loading SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Compute embeddings from ContentItem text field | numerical vectors to represent semantic meaning
    texts = [item.text for item in items] # create a list of the text attributes from each ContentItem object
    embeddings = model.encode(texts, convert_to_tensor=False) # use SentenceTransformer model to compute embeddings for each text 

    # HDBSCAN clustering
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric='euclidean')
    labels = clusterer.fit_predict(embeddings)

    # Group items based on cluster labels
    groups_dict = {}
    for idx, label in enumerate(labels):
        if label == -1:  # Ignore noise points
            continue
        if label not in groups_dict:
            groups_dict[label] = []
        groups_dict[label].append(items[idx])

    # Create ContentGroup objects
    aligned = []
    for group_items in groups_dict.values():
        references = []
        aggregated_key_concepts = []

        # Extract slide references & timestamps
        for item in group_items:
            if "slide_num" in item.metadata and item.metadata["slide_num"]:
                reference = f"Slide: {item.metadata['slide_num']}"
                if reference not in references:
                    references.append(reference)

            if "timestamp" in item.metadata and item.metadata["timestamp"]:
                reference = f"Timestamp: {item.metadata['timestamp']}"
                if reference not in references:
                    references.append(reference)

            # Aggregate key concepts from each item
            if hasattr(item, 'key_concepts'):
                aggregated_key_concepts.extend(item.key_concepts)

        # Remove duplicate key concepts
        aggregated_key_concepts = list(set(aggregated_key_concepts))

        # Generate summary
        summary = generate_summary([item.text for item in group_items], aggregated_key_concepts)

        obj = ContentGroup(
            matching_items=group_items,
            references=references,
            summary=summary
        )

        aligned.append(obj)

    return aligned

if __name__ == "__main__":
    # Create some example ContentItem objects.
    # Note: Adjust the metadata keys as per your models. Here, we use "slide_num" for slide references.
    example_items = [
        ContentItem(source="slide", text="Introduction to NLP", metadata={"slide_num": "1", "title": "Intro"}),
        ContentItem(source="transcript", text="Today we discuss natural language processing concepts.", metadata={"timestamp": "00:00:05"}),
        ContentItem(source="note", text="NLP involves the study of language data and algorithms.", metadata={"slide_num": "1"}),
        ContentItem(source="slide", text="Deep Learning Basics", metadata={"slide_num": "2", "title": "Deep Learning"}),
        ContentItem(source="transcript", text="Deep learning is a subset of machine learning.", metadata={"timestamp": "00:05:00"}),
    ]
    
    groups = align(example_items, num_clusters=3, membership_threshold=0.6)
    for idx, group in enumerate(groups):
        print(f"Group {idx+1}:")
        for item in group.matching_items:
            print("  ", item)
        print("References:", group.references)
        print("-" * 40)
