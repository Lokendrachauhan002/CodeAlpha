"""TF-IDF vectorization and cosine-similarity FAQ retrieval."""
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.preprocessor import TextPreprocessor


class FAQRetriever:
    """Fits TF-IDF to FAQ questions and finds closest matches."""

    def __init__(self, faq_path: str) -> None:
        self.preprocessor = TextPreprocessor()
        self.faqs = self._load_faqs(faq_path)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.question_matrix = self.vectorizer.fit_transform(self.faqs["processed_question"])

    def _load_faqs(self, faq_path: str) -> pd.DataFrame:
        """Load and validate the CSV dataset, then preprocess questions."""
        frame = pd.read_csv(faq_path)
        required = {"id", "category", "question", "answer"}
        if not required.issubset(frame.columns):
            raise ValueError("FAQ CSV must contain id, category, question, and answer columns.")
        frame = frame.dropna(subset=["question", "answer"]).copy()
        frame["processed_question"] = frame["question"].map(self.preprocessor.preprocess)
        return frame

    def search(self, query: str, limit: int = 3) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
        """Return best result and related FAQ suggestions, ranked by similarity."""
        processed_query = self.preprocessor.preprocess(query)
        if not processed_query:
            raise ValueError("Please enter a meaningful question using letters or words.")
        query_vector = self.vectorizer.transform([processed_query])
        scores = cosine_similarity(query_vector, self.question_matrix).flatten()
        ranked_indices = np.argsort(scores)[::-1]
        best_index = int(ranked_indices[0])
        best = self.faqs.iloc[best_index]
        confidence = round(float(scores[best_index]) * 100, 2)
        result = {"id": int(best["id"]), "category": best["category"],
                  "question": best["question"], "answer": best["answer"],
                  "confidence": confidence}
        suggestions = [{"id": int(self.faqs.iloc[i]["id"]),
                        "question": self.faqs.iloc[i]["question"],
                        "confidence": round(float(scores[i]) * 100, 2)}
                       for i in ranked_indices[1:limit + 1]]
        return result, suggestions

    def browse(self, term: str = "", limit: int = 20) -> List[Dict[str, object]]:
        """Search FAQ text for the built-in FAQ browser."""
        term = term.strip().lower()
        frame = self.faqs
        if term:
            mask = frame["question"].str.lower().str.contains(term, regex=False) | \
                   frame["category"].str.lower().str.contains(term, regex=False)
            frame = frame[mask]
        return frame[["id", "category", "question", "answer"]].head(limit).to_dict("records")
