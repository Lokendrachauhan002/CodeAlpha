"""Flask API and page routes for the offline FAQ chatbot."""
import logging
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from config import CONFIDENCE_THRESHOLD, DATASET_PATH, LOG_PATH, MAX_QUERY_LENGTH, TOP_SUGGESTIONS
from nlp.vectorizer import FAQRetriever
from utils.logger import configure_logging


def create_app(test_config=None) -> Flask:
    """Application factory so tests can create an isolated Flask instance."""
    app = Flask(__name__, template_folder=str(Path(__file__).parent.parent / "templates"),
                static_folder=str(Path(__file__).parent.parent / "static"))
    app.config.update(JSON_SORT_KEYS=False)
    if test_config:
        app.config.update(test_config)
    logger = configure_logging(LOG_PATH)
    retriever = FAQRetriever(str(DATASET_PATH))

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True)
        if not payload or not isinstance(payload.get("message"), str):
            return jsonify(error="Send JSON with a text 'message' field."), 400
        message = payload["message"].strip()
        if not message:
            return jsonify(error="Please type a question before sending."), 400
        if len(message) > MAX_QUERY_LENGTH:
            return jsonify(error=f"Question must be at most {MAX_QUERY_LENGTH} characters."), 400
        try:
            match, suggestions = retriever.search(message, TOP_SUGGESTIONS)
            understood = match["confidence"] >= CONFIDENCE_THRESHOLD
            answer = match["answer"] if understood else (
                "I am not confident enough to answer that. Please rephrase your question "
                "or try one of the suggested FAQs.")
            logger.info("Query=%r | Match=%r | Confidence=%.2f", message, match["question"], match["confidence"])
            return jsonify(answer=answer, confidence=match["confidence"], understood=understood,
                           matched_question=match["question"], category=match["category"],
                           suggestions=suggestions)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        except Exception:
            logger.exception("Chat request failed")
            return jsonify(error="Something went wrong while processing your question."), 500

    @app.get("/api/faqs")
    def faqs():
        term = request.args.get("search", "")
        return jsonify(faqs=retriever.browse(term))

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", faq_count=len(retriever.faqs))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="127.0.0.1", port=5000)
