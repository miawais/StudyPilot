from app.rag.reteriver import retrieve_relevant_chunks
from app.rag.promptbuilder import build_prompt
from app.rag.llmrunner import run_llm
import re

def is_metadata_count_query(query: str) -> str | None:
    """Detects if query is about 'how many' and returns type e.g. mcq/short_question"""
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

def is_specific_item_query(query: str) -> tuple[str, int] | None:
    """Detects if query asks for a specific number of a type"""
    query = query.lower()
    match = re.search(r'(short question|long question|mcq|activity)[^\d]*(\d+)', query)
    if match:
        type_name = match.group(1).replace(" ", "_")
        number = int(match.group(2))
        return type_name, number
    return None

def process_query(user_query: str, user_id: str = None, chat_history=None):
    retrieved_chunks = retrieve_relevant_chunks(user_query)

    #Count-based metadata queries
    type_to_count = is_metadata_count_query(user_query)
    if type_to_count:
        count = sum(1 for c in retrieved_chunks if c["metadata"].get("type") == type_to_count)
        answer = f"There are {count} {type_to_count.replace('_', ' ')}s in this chapter based on the textbook content."
        return {
            "user_id": user_id,
            "query": user_query,
            "response": answer,
            "metadata": [c["metadata"] for c in retrieved_chunks]
        }

    #Specific item request 
    item_info = is_specific_item_query(user_query)
    if item_info:
        type_name, index = item_info
        filtered = [c for c in retrieved_chunks if c["metadata"].get("type") == type_name]
        if 0 < index <= len(filtered):
            item = filtered[index - 1]
            return {
                "user_id": user_id,
                "query": user_query,
                "response": f"{type_name.replace('_', ' ').capitalize()} {index}: {item['content']}",
                "metadata": [item["metadata"]]
            }
        else:
            return {
                "user_id": user_id,
                "query": user_query,
                "response": f"Sorry, I couldn't find {type_name.replace('_', ' ')} number {index} in this chapter.",
                "metadata": []
            }

    # 3️⃣ Default: RAG flow for concept/content questions
    prompt = build_prompt(retrieved_chunks, user_query, chat_history)
    answer = run_llm(prompt)

    return {
        "user_id": user_id,
        "query": user_query,
        "response": answer,
        "metadata": [c["metadata"] for c in retrieved_chunks]
    }
