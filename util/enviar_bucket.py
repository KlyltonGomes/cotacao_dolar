from google.cloud import storage
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / "config" / ".env"

if not env_path.exists():
    raise FileNotFoundError(f".env não encontrado em {env_path}")

load_dotenv(env_path)


def enviar_para_bucket(caminho_arquivo, nome_bucket, destino_blob):

    credencial = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credencial:
        raise ValueError("Credencial não encontrada no .env")

    client = storage.Client.from_service_account_json(credencial)

    bucket = client.bucket(nome_bucket)
    blob = bucket.blob(destino_blob)

    blob.upload_from_filename(caminho_arquivo)

    print(f"✔ Upload concluído: {caminho_arquivo} → {nome_bucket}/{destino_blob}")