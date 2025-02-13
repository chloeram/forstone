"""

"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ContentItem:
    source: str                                                 # "slide"/"transcript"/"note"
    text: str                                                   # extracted text content
    metadata: Dict[str, Any]                                    # additional info - slide num, timestamp, title
    annotations: Dict[str, Any] = field(default_factory=dict)   # flexible dictionary to store later added data
    references: List[str] = field(default_factory=list)         # list to store slide or timestamp references
    key_concepts: List[str] = field(default_factory=list)
    tokens: List[str] = field(default_factory=list)

@dataclass
class ContentGroup:
    matching_items: List[ContentItem]                           # List of ContentItem objects, grouped together by semantic similarity or explicit relation
    references: List[str] = field(default_factory=list)         # List of references from input material
    summary: str = ""                                           # Text summary of key points extracted from matching items
