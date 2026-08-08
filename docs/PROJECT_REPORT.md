# Project Report: CampusAssist

## Abstract

CampusAssist is an offline college FAQ chatbot that retrieves the best answer from a curated knowledge base. It combines NLTK, spaCy, TF-IDF, and cosine similarity to accept paraphrased student questions while remaining explainable and economical.

## Introduction and problem statement

Students repeatedly ask administrative questions about admissions, fees, attendance, examinations, and facilities. Static FAQ pages require manual searching, while staff cannot provide immediate responses at all hours. The problem is to provide fast, consistent self-service answers without relying on internet-based AI services.

## Objectives

- Build an offline, beginner-friendly NLP chatbot.
- Match differently worded questions to trusted FAQ answers.
- Expose the system through a responsive web interface with confidence feedback.
- Maintain logs and provide a maintainable dataset-driven design.

## Literature survey

Rule-based chatbots use fixed patterns and are transparent but brittle. Information-retrieval chatbots rank documents using vector-space representations such as TF-IDF. Modern transformer systems can understand more context but require more compute and data. This project adopts TF-IDF retrieval because its behavior is explainable, local, and appropriate for a small controlled FAQ corpus.

## Existing and proposed system

The existing manual process depends on FAQ pages, calls, and office visits. The proposed system loads 150 validated FAQs, preprocesses their questions, ranks them against a user query, and returns the answer only when the confidence threshold is sufficient. Otherwise it requests a rephrase and shows related questions.

## Methodology and NLP pipeline

```text
User question → lowercase/remove punctuation → NLTK tokenization
→ stopword removal → spaCy lemmatization → TF-IDF vector
→ cosine similarity against all FAQ vectors → best answer + confidence
```

Lowercasing and punctuation removal reduce superficial variation. Tokenization separates words; stopword removal reduces uninformative terms; lemmatization maps forms such as “paying” toward a base form. TF-IDF gives rare, meaningful terms higher weight. Cosine similarity measures the angle between sparse vectors, yielding a score from 0 to 1, displayed as a percentage.

## System architecture

```text
Browser (Bootstrap, CSS, JavaScript)
       │ Fetch JSON
Flask routes / validation / logging
       │
FAQRetriever (preprocessor → TF-IDF → cosine ranking)
       │
CSV FAQ dataset  +  JSON reference dataset
```

## Modules and implementation

`backend/app.py` provides routes, validation, errors, and logging. `nlp/preprocessor.py` handles linguistic normalization. `nlp/vectorizer.py` loads the CSV, fits TF-IDF bigrams, ranks candidates, and creates suggestions. The frontend persists only local browser history; server logs are written to `logs/chatbot.log`.

## Testing and results

Unit tests cover preprocessing, retrieval, successful API calls, empty payloads, malformed payloads, FAQ search, and health reporting. Sample expected result: “How can I pay my fees?” should return the Fees category, payment guidance, and a high confidence score. Punctuation-only input returns HTTP 400. The small in-memory matrix provides near-instant retrieval for this dataset.

## Advantages and applications

The solution is offline, low-cost, explainable, easy to update by editing the dataset, and responsive on mobile. It can serve college helpdesks, department intranets, library support, and other bounded FAQ domains.

## Limitations and future scope

TF-IDF does not truly reason, may give low scores for vocabulary absent from the dataset, and returns only predefined answers. Future work includes multilingual FAQs, typo correction, feedback-based dataset expansion, authenticated staff administration, semantic embeddings, and analytics.

## Conclusion

CampusAssist demonstrates a practical information-retrieval chatbot using a clean, modular Python architecture. It provides trustworthy predefined answers and clearly signals low-confidence cases instead of inventing answers.

## References

1. Bird, Klein, and Loper, *Natural Language Processing with Python*, O'Reilly.
2. NLTK documentation, https://www.nltk.org/.
3. spaCy documentation, https://spacy.io/.
4. scikit-learn documentation: TF-IDF and cosine similarity, https://scikit-learn.org/.
