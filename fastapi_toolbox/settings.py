from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    应用配置类，支持从环境变量或 .env 文件加载配置

    用户可以继承此类来自定义配置：

    Example:
        ```python
        from fastapi_toolbox import Settings, init_database

        class MySettings(Settings):
            DATABASE_URL: str = "postgresql://user:pass@prod:5432/prod_db"
            JWT_SECRET_KEY: str = "my-production-secret"

        my_settings = MySettings()
        init_database(settings_instance=my_settings)
        ```
    """

    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db"

    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 默认配置实例，会自动从环境变量或 .env 文件加载
settings = Settings()
