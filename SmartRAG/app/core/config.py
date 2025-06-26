from pydantic import BaseSettings

class AppConfig(BaseSettings):
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    MODEL_NAME: str="llama3-8b-8192"
    EMBEDDING_MODEL_NAME: str="all-MiniLM-L6-v2"