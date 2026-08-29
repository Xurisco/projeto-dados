import json
import pandas as pd
from azure.storage.blob import BlobServiceClient
from src.config import AZURE_STORAGE_CONNECTION_STRING
from src.logger import logger


def upload_to_azure_lake(data, container_name: str, blob_name: str) -> None:
    """Envia dados (DataFrame ou objeto serializável) para o Azure Data Lake (ADLS Gen2)."""
    if not AZURE_STORAGE_CONNECTION_STRING:
        logger.error("A string de conexão do Azure não está configurada no .env.")
        return

    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )
        container_client = blob_service_client.get_container_client(
            container_name
        )

        # Se não existir o container, cria
        if not container_client.exists():
            container_client.create_container()

        blob_client = container_client.get_blob_client(blob_name)

        # Serializa dependendo do tipo de dado
        if isinstance(data, pd.DataFrame):
            # Se for DataFrame, podemos salvar em Parquet para alta performance no Lake
            if blob_name.endswith(".parquet"):
                output = data.to_parquet(index=False)
                blob_client.upload_blob(output, overwrite=True)
            else:
                output = data.to_json(orient="records", force_ascii=False, indent=2)
                blob_client.upload_blob(output, overwrite=True, encoding="utf-8")
        else:
            # Caso seja lista ou dicionário (JSON bruto)
            output = json.dumps(data, ensure_ascii=False, indent=2)
            blob_client.upload_blob(output, overwrite=True, encoding="utf-8")

        logger.info(
            "Arquivo '%s' enviado com sucesso para o container '%s' (Azure).",
            blob_name,
            container_name,
        )
    except Exception as e:
        logger.error(
            "Erro ao enviar arquivo para o Azure Blob Storage: %s", str(e)
        )