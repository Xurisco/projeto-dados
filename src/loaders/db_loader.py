import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL
from src.logger import logger


def save_to_db(df: pd.DataFrame, table_name: str) -> None:
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        connection.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    product_id INT PRIMARY KEY,
                    sku VARCHAR(50),
                    name VARCHAR(255),
                    category VARCHAR(100),
                    subcategory VARCHAR(100),
                    brand VARCHAR(100),
                    total_orders INT,
                    total_quantity INT,
                    total_revenue FLOAT,
                    total_cost FLOAT,
                    total_profit FLOAT,
                    margin_percent FLOAT,
                    total_shipping FLOAT
                );
                """
            )
        )

    # Atualiza ou insere registros
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    logger.info("Tabela '%s' atualizada no PostgreSQL com sucesso.", table_name)