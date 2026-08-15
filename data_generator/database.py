from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus

from data_generator.config import (
    SQLSERVER_HOST,
    SQLSERVER_PORT,
    SQLSERVER_DATABASE,
    SQLSERVER_USER,
    SQLSERVER_PASSWORD,
    SQLSERVER_DRIVER,
)


def get_connection_string() -> str:
    if not SQLSERVER_PASSWORD:
        raise ValueError("SQLSERVER_PASSWORD no está definido en el archivo .env")

    odbc_string = (
        f"DRIVER={{{SQLSERVER_DRIVER}}};"
        f"SERVER={SQLSERVER_HOST},{SQLSERVER_PORT};"
        f"DATABASE={SQLSERVER_DATABASE};"
        f"UID={SQLSERVER_USER};"
        f"PWD={SQLSERVER_PASSWORD};"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
    )

    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_string)}"


def get_engine() -> Engine:
    return create_engine(get_connection_string(), fast_executemany=True)