import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL
from src.logger import logger

def save_to_db(df: pd.DataFrame, table_name: str) -> None:
   
    engine = create_engine(DATABASE_URL)
    
    df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
    logger.info("Tabela '%s' atualizada no PostgreSQL com sucesso.", table_name)