from pathlib import Path


BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")
IDS_PATH = Path("data/metadata/ids.json")

CUSTOMERS_PER_RUN = 10
PRODUCTS_PER_RUN = 5
ORDERS_PER_RUN = 50

PIPELINE_INTERVAL = 30

import os

# Configurações do PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")