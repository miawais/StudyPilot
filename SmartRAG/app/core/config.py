from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # External API Keys
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str

    # Defaults
    MODEL_NAME: str = "llama3-8b-8192"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Auth Secret
    JWT_SECRET: str = "supersecret"  

config = AppConfig()
