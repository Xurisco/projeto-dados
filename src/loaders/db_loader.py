import time
import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL
from src.logger import logger


def save_to_db(df: pd.DataFrame, table_name: str) -> None:
    engine = create_engine(DATABASE_URL)

    # Tenta conectar e salvar até 5 vezes se o banco estiver subindo
    for attempt in range(1, 6):
        try:
            df.to_sql(table_name, con=engine, if_exists="replace", index=False)
            logger.info("Tabela '%s' atualizada no PostgreSQL com sucesso.", table_name)
            return
        except Exception as e:
            logger.warning(
                "Aguardando PostgreSQL responder (Tentativa %d/5)... Erro: %s",
                attempt,
                e,
            )
            time.sleep(3)

    logger.error("Falha crítica ao gravar a tabela '%s' no banco.", table_name)