from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DB: str
#     DB_HOST: str = "db"
#     DB_PORT: int = 5432

#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

#     # This is not a Pydantic Field, just a property function
#     @property
#     def DATABASE_URL(self) -> str:
#         return (
#             f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
#             f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
#         )

#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# # Instantiate
# settings = Settings()


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
