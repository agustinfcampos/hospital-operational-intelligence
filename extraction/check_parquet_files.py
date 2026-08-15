from datetime import datetime
from pathlib import Path

import pandas as pd


RAW_OUTPUT_PATH = Path("extraction/output/raw")

TABLES_TO_CHECK = [
    "specialties",
    "medical_centers",
    "insurance_plans",
    "patients",
    "doctors",
    "appointments",
    "procedures",
    "billing",
]


def main() -> None:
    extraction_date = datetime.now().strftime("%Y-%m-%d")

    print("Validando archivos Parquet generados")
    print(f"Fecha de extracción: {extraction_date}")

    for table_name in TABLES_TO_CHECK:
        parquet_file = (
            RAW_OUTPUT_PATH
            / table_name
            / f"extraction_date={extraction_date}"
            / f"{table_name}.parquet"
        )

        if not parquet_file.exists():
            print(f"[ERROR] No existe archivo para tabla: {table_name}")
            continue

        df = pd.read_parquet(parquet_file)

        print(f"{table_name}: {len(df)} registros, {len(df.columns)} columnas")


if __name__ == "__main__":
    main()