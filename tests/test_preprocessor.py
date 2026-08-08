"""Unit tests for preprocessing and retrieval."""
import unittest

from config import DATASET_PATH
from nlp.preprocessor import TextPreprocessor
from nlp.vectorizer import FAQRetriever


class NLPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preprocessor = TextPreprocessor()
        cls.retriever = FAQRetriever(str(DATASET_PATH))

    def test_preprocess_removes_stopwords_and_punctuation(self):
        result = self.preprocessor.preprocess("How do I pay the fees?")
        self.assertNotIn("the", result.split())
        self.assertNotIn("?", result)

    def test_retriever_finds_relevant_result(self):
        result, _ = self.retriever.search("I need to make a tuition payment")
        self.assertEqual(result["category"], "Fees")


if __name__ == "__main__":
    unittest.main()
