"""Text cleaning, tokenization, stopword removal, and lemmatization."""
import re
import string
from typing import List

import nltk
import spacy
from nltk.corpus import stopwords


class TextPreprocessor:
    """Normalizes text consistently for FAQ matching."""

    def __init__(self) -> None:
        self._ensure_nltk_resources()
        self.stop_words = set(stopwords.words("english"))
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
        except OSError:
            # Keeps the project usable when the optional spaCy model is absent.
            self.nlp = spacy.blank("en")

    @staticmethod
    def _ensure_nltk_resources() -> None:
        """Download small NLTK resources once when not already installed."""
        for resource, path in [("punkt", "tokenizers/punkt"), ("punkt_tab", "tokenizers/punkt_tab"),
                               ("stopwords", "corpora/stopwords")]:
            try:
                nltk.data.find(path)
            except LookupError:
                nltk.download(resource, quiet=True)

    def tokenize(self, text: str) -> List[str]:
        """Lowercase, strip punctuation, tokenize, and remove stopwords."""
        lowered = text.lower().translate(str.maketrans("", "", string.punctuation))
        cleaned = re.sub(r"\s+", " ", lowered).strip()
        tokens = nltk.word_tokenize(cleaned)
        return [token for token in tokens if token.isalpha() and token not in self.stop_words]

    def lemmatize(self, tokens: List[str]) -> List[str]:
        """Return spaCy lemmas; safely falls back to tokens without its model."""
        doc = self.nlp(" ".join(tokens))
        return [token.lemma_ if token.lemma_ not in {"", "-PRON-"} else token.text
                for token in doc]

    def preprocess(self, text: str) -> str:
        """Return a space-separated normalized representation for TF-IDF."""
        return " ".join(self.lemmatize(self.tokenize(text)))
