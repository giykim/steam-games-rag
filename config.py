import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

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

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database tables
OPEN_AI_DESCRIPTION_TABLE = "description_embeddings_openai"
OPEN_AI_STATS_TABLE = "stats_embeddings_openai"
SENTENCE_TRANSFORMER_DESCRIPTION_TABLE = "description_embeddings_st"
SENTENCE_TRANSFORMER_STATS_TABLE = "stats_embeddings_st"
