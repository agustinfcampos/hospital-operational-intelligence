import os
from pathlib import Path

import boto3
from dotenv import load_dotenv


load_dotenv()


LOCAL_RAW_PATH = Path("extraction/output/raw")

AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def get_s3_client():
    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME no está definido en el archivo .env")

    return boto3.client("s3", region_name=AWS_REGION)


def upload_file_to_s3(local_file: Path, s3_client) -> None:
    relative_path = local_file.relative_to(LOCAL_RAW_PATH)

    s3_key = f"raw/{relative_path.as_posix()}"

    print(f"Subiendo: {local_file}")
    print(f"Destino: s3://{S3_BUCKET_NAME}/{s3_key}")

    s3_client.upload_file(
        Filename=str(local_file),
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
    )


def main() -> None:
    if not LOCAL_RAW_PATH.exists():
        raise FileNotFoundError(
            f"No existe la carpeta local de raw: {LOCAL_RAW_PATH}"
        )

    s3_client = get_s3_client()

    parquet_files = list(LOCAL_RAW_PATH.rglob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(
            f"No se encontraron archivos Parquet en {LOCAL_RAW_PATH}"
        )

    print("Iniciando carga de Parquet local a S3 raw")
    print(f"Bucket destino: {S3_BUCKET_NAME}")
    print(f"Región: {AWS_REGION}")
    print(f"Archivos encontrados: {len(parquet_files)}")

    for parquet_file in parquet_files:
        upload_file_to_s3(parquet_file, s3_client)

    print("Carga a S3 finalizada correctamente.")


if __name__ == "__main__":
    main()