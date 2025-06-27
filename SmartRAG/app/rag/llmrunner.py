from groq import Groq
from app.core.config import config

client = Groq(api_key=config.GROQ_API_KEY)

def run_llm(prompt: str):
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful AI tutor for 9th grade computer science."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()
