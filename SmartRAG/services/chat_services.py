from rag.retriever import retrieve_relevant_chunks
from rag.prompt_builder import build_prompt
from rag.llm_runner import run_llm

def process_query(user_query: str, user_id: str = None, chat_history=None):
    chunks = retrieve_relevant_chunks(user_query)
    prompt = build_prompt(chunks, user_query, chat_history)
    answer = run_llm(prompt)
    return {
        "user_id": user_id,
        "query": user_query,
        "response": answer,
        "metadata": [c["metadata"] for c in chunks]
    }
