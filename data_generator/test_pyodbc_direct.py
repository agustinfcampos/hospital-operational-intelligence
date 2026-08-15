import pyodbc


connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:127.0.0.1,14330;"
    "DATABASE=hospital_oltp;"
    "UID=sa;"
    "PWD=Hospital_2026;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

print("Probando conexión directa con pyodbc...")

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME")
    rows = cursor.fetchall()

    print("Conexión correcta. Tablas encontradas:")
    for row in rows:
        print(f"- {row.TABLE_NAME}")