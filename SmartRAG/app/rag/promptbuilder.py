def build_prompt(context_chunks, user_query, chat_history=None):
    context = "\n---\n".join([
        f"[{c['metadata'].get('chapter')} > {c['metadata'].get('topic')} > {c['metadata'].get('subtopic')} | {c['metadata'].get('type')}]\n{c['content']}"
        for c in context_chunks if c.get("content")
    ])

    history = ""
    if chat_history:
        history = "\n".join([f"{h['role'].capitalize()}: {h['message']}" for h in chat_history])
    
    return f"""
You are a helpful AI tutor for 9th grade Computer Science. Be accurate, do not hallucinate.

Chat History:
{history}

Context:
{context}

User Question:
{user_query}

Answer:"""
