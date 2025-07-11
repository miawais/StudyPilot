from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    MODEL_NAME: str = "llama3-8b-8192"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        extra = "ignore"  


class Settings(BaseSettings):
    JWT_SECRET: str

    class Config:
        env_file = ".env"
        extra = "ignore"  


config = AppConfig()
settings = Settings()
