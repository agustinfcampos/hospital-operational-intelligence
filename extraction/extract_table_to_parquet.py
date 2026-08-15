from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from data_generator.database import get_engine


RAW_OUTPUT_PATH = Path("extraction/output/raw")

TABLES_TO_EXTRACT = [
    "specialties",
    "medical_centers",
    "insurance_plans",
    "patients",
    "doctors",
    "appointments",
    "procedures",
    "billing",
]


def extract_table(table_name: str, extraction_date: str) -> None:
    engine = get_engine()

    output_dir = RAW_OUTPUT_PATH / table_name / f"extraction_date={extraction_date}"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{table_name}.parquet"

    query = text(f"SELECT * FROM dbo.{table_name}")

    print(f"Extrayendo tabla: {table_name}")

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    df.to_parquet(output_file, index=False)

    print(f"Archivo generado: {output_file}")
    print(f"Registros extraídos: {len(df)}")


def main() -> None:
    extraction_date = datetime.now().strftime("%Y-%m-%d")

    print("Iniciando extracción SQL Server → Parquet local")
    print(f"Fecha de extracción: {extraction_date}")

    for table_name in TABLES_TO_EXTRACT:
        extract_table(table_name, extraction_date)

    print("Extracción finalizada correctamente.")


if __name__ == "__main__":
    main()