# Viva Preparation: 40 Questions and Answers

## 1. What is NLP?

Natural Language Processing is the field that enables software to analyse, represent, and generate human language. In this project it turns a natural student question into a comparable text representation.

## 2. What is a chatbot?

A chatbot is an interactive program that accepts messages and returns responses. CampusAssist is a retrieval-based chatbot because it selects from approved FAQ answers rather than generating new text.

## 3. What is the difference between rule-based and retrieval chatbots?

Rule-based bots depend on manually written patterns; retrieval bots rank stored answers using similarity. Retrieval supports more wording variation without needing a rule for every sentence.

## 4. Why is this chatbot offline?

Its dataset, NLP libraries, TF-IDF matrix, and Flask server run locally. It makes no calls to a model API or paid cloud service.

## 5. What is tokenization?

Tokenization splits text into units, usually words. For example, a question about paying fees becomes individual tokens that later processing can inspect.

## 6. Why convert text to lowercase?

Lowercasing treats equivalent forms such as Fees and fees as the same token, reducing unnecessary vocabulary size.

## 7. Why remove punctuation?

Punctuation often adds no meaning to a short FAQ query. Removing it lets 'fees?' and 'fees' compare consistently.

## 8. What are stopwords?

Stopwords are common words such as 'the', 'is', and 'how'. Removing them usually focuses matching on informative domain words.

## 9. What is lemmatization?

Lemmatization maps inflected words to a base form, such as 'studies' to 'study'. Unlike simple stemming, it aims to preserve valid linguistic forms.

## 10. How are NLTK and spaCy used here?

NLTK provides word tokenization and English stopwords. spaCy performs lemmatization; a safe blank-language fallback keeps the app usable when its model is not installed.

## 11. What is TF-IDF?

Term Frequency–Inverse Document Frequency weights a word by its importance in one document and rarity across all documents. Rare terms such as 'revaluation' become more influential than common terms.

## 12. What does TF in TF-IDF mean?

Term frequency measures how often a term occurs in one document. It is one component of the final TF-IDF weight.

## 13. What does IDF mean?

Inverse document frequency reduces the weight of terms that occur in many documents and increases the value of distinctive terms.

## 14. Why use n-grams?

N-grams represent adjacent word sequences. The project uses unigrams and bigrams, allowing phrases such as 'fee payment' to carry more meaning than separate words alone.

## 15. What is vectorization?

Vectorization converts text into numerical feature vectors that machine-learning and similarity algorithms can process.

## 16. What is cosine similarity?

Cosine similarity measures the cosine of the angle between two vectors. It is useful for text because it compares word-weight direction rather than merely document length.

## 17. What range does cosine similarity have here?

For non-negative TF-IDF vectors it is normally between 0 and 1. The application multiplies the best score by 100 to show a confidence percentage.

## 18. Is cosine score a probability?

No. It is a similarity measure, not a calibrated probability. The confidence label is an understandable UI indicator and the threshold must be tuned using test queries.

## 19. Why is a confidence threshold needed?

It prevents the bot from confidently presenting a loosely related answer. Below the threshold the bot requests a rephrased question and offers suggestions.

## 20. How are related questions created?

After sorting all cosine scores, the application returns the next highest-ranked FAQ questions as suggestions.

## 21. What is information retrieval?

Information retrieval finds and ranks relevant items from a collection. The FAQ retriever ranks stored questions against the user's query.

## 22. What is a corpus in this project?

The corpus is the collection of all FAQ questions used to fit the TF-IDF vectorizer.

## 23. Why fit the vectorizer on FAQ questions?

Fitting learns the vocabulary and IDF weights of the approved knowledge base. A user query is then transformed in that same feature space.

## 24. What happens with an unseen word?

A word not in the fitted vocabulary contributes no feature to the query vector. This is one reason the bot may return low confidence for novel topics.

## 25. What is Flask?

Flask is a lightweight Python web framework. It serves the HTML page and provides JSON API routes for chat, FAQ search, and health checks.

## 26. What is a REST API endpoint?

It is a URL that exposes a specific service operation. For example, POST /api/chat accepts a message and returns a structured JSON result.

## 27. Why use POST for chat?

A chat request sends user content in a JSON body and performs a processing operation; POST is appropriate for that request shape.

## 28. What validation is performed?

The API requires JSON with a string message, trims whitespace, rejects empty input, applies a maximum length, and reports processing errors safely.

## 29. What is JSON?

JSON is a lightweight key-value data format. Flask uses it to communicate structured answers, confidence, category, and suggestions to JavaScript.

## 30. How does the frontend communicate with Flask?

Browser JavaScript uses the Fetch API to send a JSON POST request and then updates chat bubbles with the JSON response.

## 31. Why separate backend, NLP, and utility modules?

Separation of concerns makes each component easier to read, test, replace, and maintain. The route layer does not need to contain TF-IDF implementation details.

## 32. What is object-oriented design used for?

TextPreprocessor encapsulates normalization behavior and FAQRetriever encapsulates data loading and search state. Their methods provide clean reusable interfaces.

## 33. Why log chatbot queries?

Logs help administrators identify common questions, low-confidence requests, and failures. They can guide FAQ improvements while respecting privacy policy.

## 34. What is unit testing?

Unit testing checks small, deterministic pieces of code automatically. The project tests preprocessing, retrieval, API success, invalid inputs, search, and health reporting.

## 35. What are edge cases for this system?

Examples include empty text, punctuation-only input, malformed JSON, very long messages, unseen terminology, a missing CSV column, and two FAQs with similar wording.

## 36. What is PEP 8?

PEP 8 is Python's style guide. Consistent names, spacing, imports, docstrings, and line lengths improve readability and team maintenance.

## 37. What is a virtual environment?

A virtual environment isolates project packages from the system Python installation, making setup reproducible and avoiding dependency conflicts.

## 38. How would you improve accuracy?

Add representative FAQ variants, tune the threshold on labelled queries, correct spelling, improve data quality, and optionally move to local semantic embeddings after evaluation.

## 39. What are the limitations of TF-IDF?

It relies on word overlap and cannot deeply understand context, negation, or world knowledge. It also cannot answer questions absent from the curated data.

## 40. How can the FAQ dataset be maintained?

Authorized staff can add clear question-answer pairs in CSV, keep IDs unique, retain required columns, and restart the app so it rebuilds the TF-IDF index.
