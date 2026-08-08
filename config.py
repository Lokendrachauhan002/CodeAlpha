"""Central configuration for the FAQ chatbot."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "college_faqs.csv"
LOG_PATH = BASE_DIR / "logs" / "chatbot.log"
CONFIDENCE_THRESHOLD = 18.0
TOP_SUGGESTIONS = 3
MAX_QUERY_LENGTH = 500
