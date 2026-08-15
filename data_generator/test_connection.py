from sqlalchemy import text

from data_generator.database import get_engine


def main() -> None:
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME")
        )

        print("Conexión correcta. Tablas encontradas:")
        for row in result:
            print(f"- {row.TABLE_NAME}")


if __name__ == "__main__":
    main()
