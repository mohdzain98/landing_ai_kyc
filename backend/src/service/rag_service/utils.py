import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv


class Logger:
    @staticmethod
    def get_logger(name: str | None = None) -> logging.Logger:
        """Return a configured logger.

        - Logs to stdout
        - Simple, beginner-friendly format
        - Default level INFO (override via LOG_LEVEL env or code if needed)
        """
        logger = logging.getLogger(name if name else __name__)
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.propagate = False
        return logger


class Config:
    def __init__(self, dotenv_filename: str = ".env"):
        dotenv_path = self._find_env_file(dotenv_filename)
        logger = Logger.get_logger()
        if dotenv_path:
            load_dotenv(dotenv_path)
            logger.info(f"Loaded environment from: {dotenv_path}")
        else:
            logger.warning(".env file not found in current or parent directories.")

        self.gemini_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY", "")
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY", "")

    def _find_env_file(self, filename: str) -> str | None:
        """Search current and parent directories for the .env file."""
        current_dir = Path(__file__).resolve().parent
        for parent in [current_dir, *current_dir.parents]:
            env_path = parent / filename
            if env_path.exists():
                return str(env_path)
        return None
