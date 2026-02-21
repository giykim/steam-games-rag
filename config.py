import logging
import os
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s - %(message)s"
)

# Project root path
PROJECT_ROOT_PATH = Path(__file__).resolve().parent

# Data paths
PROCESSED_DATA_PATH = PROJECT_ROOT_PATH / "data" / "processed"
RAW_DATA_PATH = PROJECT_ROOT_PATH / "data" / "raw"

# Database url
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/steam_games")
