import pinecone
import re
from rag.embedder import embed_text
from core.config import config

pinecone.init(api_key=config.PINECONE_API_KEY, environment=config.PINECONE_ENVIRONMENT)
index = pinecone.Index(config.PINECONE_INDEX_NAME)

def extract_metadata_from_query(query: str):
    query = query.lower()
    metadata = {}

    if "chapter 1" in query or "unit 1" in query:
        metadata["chapter"] = "Unit 1: Problem Solving"

    topic_match = re.search(r"\b1\.\d+\b", query)
    if topic_match:
        topic_num = topic_match.group()
        metadata["topic"] = f"{topic_num} Flowcharts" if "flowchart" in query else f"{topic_num}"

    if "importance" in query:
        metadata["subtopic"] = "1.2.2 Importance of Flowcharts in Problem Solving"
    elif "requirements" in query:
        metadata["subtopic"] = "1.2.3 Determining Requirements for a Flowchart"
    elif "symbols" in query:
        metadata["subtopic"] = "1.2.4 Using Flowchart Symbols"

    if "activity" in query:
        metadata["type"] = "activity"
    elif "mcq" in query:
        metadata["type"] = "mcq"
    elif "short question" in query:
        metadata["type"] = "short_question"
    elif "long question" in query:
        metadata["type"] = "long_question"

    return metadata

def retrieve_relevant_chunks(query, top_k=30, filter_meta=None):
    query_vector = embed_text(query)

    if filter_meta is None:
        filter_meta = extract_metadata_from_query(query)

    print("🧠 Metadata Filter Applied:", filter_meta)

    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        filter=filter_meta
    )

    return [
        {
            "content": match["metadata"].get("text", ""),
            "metadata": match.get("metadata", {})
        }
        for match in response.get("matches", [])
    ]
