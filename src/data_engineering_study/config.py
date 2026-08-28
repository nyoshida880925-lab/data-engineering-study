import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / "docker" / "postgres" / ".env"

load_dotenv(ENV_PATH)

def get_postgres_settings() -> dict[str, str]:
    required_settings = {
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
    }

    missing_settings = [
        setting
        for setting in required_settings
        if not os.getenv(setting)
    ]
    if missing_settings:
        raise RuntimeError(
            f"環境変数が不足しています: {', '.join(sorted(missing_settings))}"
        )

    return {setting: os.environ[setting] for setting in required_settings}

def get_s3_settings() -> dict[str, str]:
    load_dotenv(PROJECT_ROOT / ".env")

    required_settings = {
        "AWS_REGION",
        "S3_BUCKET",
    }

    missing_settings = [
        setting
        for setting in required_settings
        if not os.getenv(setting)
    ]
    if missing_settings:
        raise RuntimeError(
            f"環境変数が不足しています: {', '.join(sorted(missing_settings))}"
        )

    return {setting: os.environ[setting] for setting in required_settings}
