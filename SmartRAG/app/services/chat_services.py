import re
from typing import Optional, Tuple, List
from app.rag.reteriver import retrieve_relevant_chunks
from app.rag.promptbuilder import build_prompt
from app.rag.llmrunner import run_llm
from app.db.database import SessionLocal
from app.db.models import ChatLog,User

# Detect count-based queries (e.g., "how many MCQs?")
def is_metadata_count_query(query: str) -> Optional[str]:
    query = query.lower()
    if "how many" in query:
        if "mcq" in query or "multiple choice" in query:
            return "mcq"
        if "short question" in query:
            return "short_question"
        if "long question" in query:
            return "long_question"
        if "activity" in query:
            return "activity"
    return None

# Detect item-specific queries (e.g., "What is MCQ 2?")
def is_specific_item_query(query: str) -> Optional[Tuple[str, int]]:
    query = query.lower()
    match = re.search(r'(short question|long question|mcq|activity)[^\d]*(\d+)', query)
    if match:
        type_name = match.group(1).replace(" ", "_")
        number = int(match.group(2))
        return type_name, number
    return None

# Return only top-1 scoring chunk metadata
def clean_top_metadata(chunks: List[dict], top_k: int = 1) -> List[dict]:
    top_chunks = sorted(
        chunks,
        key=lambda c: c["metadata"].get("score", 0),
        reverse=True
    )[:top_k]
    return [
        {
            "chapter": c["metadata"].get("chapter"),
            "topic": c["metadata"].get("topic"),
            "subtopic": c["metadata"].get("subtopic"),
            "type": c["metadata"].get("type"),
            "score": c["metadata"].get("score"),
        }
        for c in top_chunks
    ]

def process_query(user_query: str, user: User, chat_history=None):
    user_id = str(user.id)
    username = user.username

    retrieved_chunks = retrieve_relevant_chunks(user_query)

    # Count-based query
    type_to_count = is_metadata_count_query(user_query)
    if type_to_count:
        count = sum(1 for c in retrieved_chunks if c["metadata"].get("type") == type_to_count)
        answer = f"There are {count} {type_to_count.replace('_', ' ')}s in this chapter based on the textbook content."
        log_chat(user_id, user_query, answer, clean_top_metadata(retrieved_chunks), username=username)
        return {
            "user_id": user_id,
            "username": username,
            "query": user_query,
            "response": answer,
            "metadata": clean_top_metadata(retrieved_chunks),
        }

    # Specific item query
    item_info = is_specific_item_query(user_query)
    if item_info:
        type_name, index = item_info
        filtered = [c for c in retrieved_chunks if c["metadata"].get("type") == type_name]
        if 0 < index <= len(filtered):
            item = filtered[index - 1]
            response = f"{type_name.replace('_', ' ').capitalize()} {index}: {item['content']}"
            log_chat(user_id, user_query, response, clean_top_metadata([item]), username=username)
        else:
            response = f"Sorry, I couldn't find {type_name.replace('_', ' ')} number {index} in this chapter."
            log_chat(user_id, user_query, response, [], username=username)
        return {
            "user_id": user_id,
            "username": username,
            "query": user_query,
            "response": response,
            "metadata": clean_top_metadata([item]) if index <= len(filtered) else [],
        }

    # Freeform content-based query
    prompt = build_prompt(retrieved_chunks, user_query, chat_history)
    answer = run_llm(prompt)
    log_chat(user_id, user_query, answer, clean_top_metadata(retrieved_chunks), username=username)

    return {
        "user_id": user_id,
        "username": username,
        "query": user_query,
        "response": answer,
        "metadata": clean_top_metadata(retrieved_chunks),
    }


# Save chat log to DB
def log_chat(user_id, user_query, response, metadata, username=None):
    db = SessionLocal()
    log = ChatLog(
        user_id=user_id,
        username=username,  
        query=user_query,
        response=response,
        chunk_metadata=metadata
    )
    db.add(log)
    db.commit()
    db.close()

