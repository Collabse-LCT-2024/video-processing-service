import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '../../.env'),
                                      env_file_encoding='utf-8')
    project_name: str = Field(..., alias="PROJECT_NAME", env="PROJECT_NAME"
                              )
    description: str = Field(
        ...,
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )

    QDRANT_COLLECTION_NAME: str = Field(..., alias="QDRANT_COLLECTION_NAME", env="QDRANT_COLLECTION_NAME")

    kafka_video_processing_requests_topic: str = Field(
        ..., alias="KAFKA_VIDEO_PROCESSING_REQUESTS_TOPIC",
        env="KAFKA_VIDEO_PROCESSING_REQUESTS_TOPIC"
    )

    EMBEDDING_API_URL: str = Field(..., alias="EMBEDDING_API_URL",
                                   env="EMBEDDING_API_URL")

    KAFKA_HOST: str = Field(..., alias="KAFKA_HOST", env="KAFKA_HOST")
    KAFKA_PORT: int = Field(..., alias="KAFKA_PORT", env="KAFKA_PORT")
    KAFKA_GROUP: str = Field(..., alias="KAFKA_GROUP", env="KAFKA_GROUP")

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
