from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "RAG Document Intelligence Platform"
    app_env: str = "development"
    app_version: str = "1.0.0"
    debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_url: str = "http://localhost:8000"

    streamlit_port: int = 8501

    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.1

    chroma_persist_directory: str = "./data/chroma"
    chroma_collection_name: str = "business_documents"

    upload_directory: str = "./data/uploads"
    metadata_directory: str = "./data/metadata"

    max_file_size_mb: int = 25
    chunk_size: int = 1000
    chunk_overlap: int = 200
    default_top_k: int = 5

    log_level: str = "INFO"
    cors_origins: list[str] = ["*"]

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_directory).resolve()

    @property
    def metadata_path(self) -> Path:
        return Path(self.metadata_directory).resolve()


settings = Settings()
