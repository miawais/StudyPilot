from sentence_transformers import SentenceTransformer
from app.core.config import config

model = SentenceTransformer(config.EMBEDDING_MODEL)

def embed_text(text: str):
    return model.encode(text).tolist()
