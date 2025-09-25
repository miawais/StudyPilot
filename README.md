# StudyPilot: AI-Powered Learning Companion for Students

StudyPilot is an AI-driven educational platform designed to align students with their curriculum, streamline exam preparation, and personalize learning experiences. It leverages state-of-the-art Large Language Models (LLMs), smart retrieval techniques, and structured educational content to deliver precise, curriculum-aligned responses.

---

## Core Features

* **Curriculum-Aware Q\&A**: Ask any question from your textbook and get precise, source-aligned answers.
* **Smart Retrieval (RAG)**: Uses vector search with metadata filtering for accurate context selection.
* **Chapter/Exercise Analysis**: Extracts MCQs, short questions, activities, and more from any chapter.
* **Intent-Aware Query Processing**: Handles a wide range of query types (e.g., "What is Activity 1.2?" or "List all short questions in Unit 3").
* **Study Outcome Alignment**: Maps user learning progress to official learning outcomes.
* **Feedback Loop**: Captures user feedback to refine system behavior over time.

---

## Impact

StudyPilot helps students

* Stay aligned with educational outcomes and syllabus goals
* Understand and revise textbook content more efficiently
* Practice exam-style questions in context
* Minimize learning gaps with interactive content understanding

---

## Tech Stack

### AI & NLP

* **LLMs**: LLaMA 3 (via GROQ), Gemini 1.5 Pro (Google AI Studio)
* **Embeddings**: Sentence Transformers (MiniLM, BGE)
* **Prompting**: Dynamic system prompt with embedded context chunks

### Data Processing

* **Sources**: DOCX / Scanned PDFs (OCR supported)
* **Pipeline**: Chunking, cleaning, metadata tagging (chapter, topic, type)
* **Schema**: JSON with nested metadata

### Retrieval System

* **Vector Store**: Pinecone (384D embeddings)
* **Filtering**: Multi-key metadata filtering (chapter, type, subtopic, etc.)
* **Retriever**: Hybrid dense search with fallback strategies

### MLOps

* **Versioning**: DVC for datasets & vector versions
* **Monitoring**: Weights & Biases / MLflow for prompt evaluations
* **Logging**: Query, retrieved context, prompt, and response tracking
* **Feedback Loop**: Intent + outcome evaluation from users

### Platform Infrastructure

* **Backend**: Python (FastAPI planned)
* **UI**: CLI / Jupyter prototype (React Web App planned)
* **Deployment**: Docker, optional Kubernetes
* **Security**: Metadata-sanitized prompts, response auditing, privacy-first design

---

## Example Pipeline Flow

1. **User Input**: "What is Activity 1.2 in Chapter 1?"
2. **Query Preprocessing**: Normalization + Intent Parsing
3. **Retriever**: Searches Pinecone using vector + metadata filter (e.g., `chapter=Unit 1`, `type=activity`)
4. **Prompt Builder**: Chunks + User Query combined into structured LLM prompt
5. **LLM**: Generates aligned, source-anchored response
6. **Feedback Capture**: Response logged + user satisfaction recorded

---

## Dataset Format

```json
{
  "content": "A well-defined problem is the one that does not contain ambiguities...",
  "metadata": {
    "subject": "Computer Science",
    "grade": "9",
    "book_name": "Computer Science & IT",
    "language": "English",
    "chapter": "Unit 1: Problem Solving",
    "topic": "1.1 Problem Solving Steps",
    "subtopic": "1.1.1 Defining a Problem",
    "type": "theory",
    "question_number": "",
    "question_type": "",
    "activity_number": ""
  }
}
```

---

## Future Plans

* ✅ Add full UI-based experience (student dashboard, quiz mode)
* ✅ Model feedback tuning with Reinforcement Learning from Human Feedback (RLHF)
* ✅ Multilingual support (Urdu, Punjabi, Sindhi)
* ✅ Analytics for teachers (learning progress dashboard)

---

## Author

**Awais** - AI Engineer | Creator of StudyPilot

---

## Contributing

Pull requests are welcome! For feature ideas or bug reports, please open an issue.

---

[MIT](LICENSE)

---

> Empowering every student with AI to unlock their full academic potential.


