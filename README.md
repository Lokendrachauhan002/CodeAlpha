# CampusAssist: Offline AI FAQ Chatbot

CampusAssist is a B.Tech AI/ML-ready FAQ chatbot for a college management system. It uses local NLP only: NLTK preprocessing, spaCy lemmatization, scikit-learn TF-IDF, and cosine similarity. No API key, paid cloud service, or generative AI model is required.

## Features

- 150 realistic college FAQs in CSV and JSON
- NLP normalization: lowercase, punctuation removal, tokenization, stopword removal, and lemmatization
- TF-IDF bigrams with cosine-similarity matching, confidence score, threshold fallback, and related questions
- Flask JSON API, input validation, error handling, and query/response-match logging
- Responsive Bootstrap chat UI with dark mode, typing cue, timestamps, browser-local history, search, clear, and TXT export

## Quick start on Windows / VS Code

1. Install Python 3.10+ and open this folder in VS Code.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install packages and the recommended spaCy English model:

   ```powershell
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. Start the server, then visit `http://127.0.0.1:5000`.

   ```powershell
   python run.py
   ```

NLTK resources download automatically the first time. The app still runs if the spaCy model is unavailable, but installing it provides better lemmatization.

## Project structure

```text
FAQ Chatbot/
├── backend/app.py              # Flask routes and API validation
├── nlp/preprocessor.py         # NLTK + spaCy text normalization
├── nlp/vectorizer.py           # TF-IDF and cosine retrieval
├── utils/logger.py             # File/console logging
├── dataset/college_faqs.{csv,json}
├── templates/index.html
├── static/css/style.css
├── static/js/app.js
├── tests/                      # Unit and API tests
├── docs/PROJECT_REPORT.md
├── docs/VIVA_QUESTIONS.md
└── run.py
```

## API

`POST /api/chat` body: `{"message":"How can I pay my fees?"}`. The response includes `answer`, `confidence`, `understood`, `matched_question`, `category`, and `suggestions`.

`GET /api/faqs?search=library` searches the FAQ browser. `GET /api/health` reports readiness and dataset count.

## Testing and sample queries

```powershell
python -m unittest discover -s tests -v
```

Try: “How can I pay my fees?”, “I forgot my portal password”, “Can I renew a library book?”, and “What is the minimum attendance?”. Empty input, non-JSON bodies, 500+ character messages, and punctuation-only messages are handled with clear errors.

## Deployment

See [deployment instructions](docs/DEPLOYMENT.md), [project report](docs/PROJECT_REPORT.md), and [viva guide](docs/VIVA_QUESTIONS.md). Screenshot placeholders are in `docs/screenshots/`—add your own running application captures there before submission.

## Future enhancements

Add an admin FAQ editor, multilingual support, spell correction, authentication, analytics dashboard, and a curated feedback loop for unanswered questions.
