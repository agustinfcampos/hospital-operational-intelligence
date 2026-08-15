from sqlalchemy import text

from data_generator.database import get_engine


SPECIALTIES = [
    ("Cardiología", "Clínica"),
    ("Clínica Médica", "Clínica"),
    ("Traumatología", "Quirúrgica"),
    ("Pediatría", "Clínica"),
    ("Neurología", "Clínica"),
    ("Dermatología", "Clínica"),
    ("Ginecología", "Clínica"),
    ("Oftalmología", "Clínica"),
    ("Guardia Adultos", "Emergencias"),
    ("Guardia Pediátrica", "Emergencias"),
    ("Diagnóstico por Imágenes", "Diagnóstico"),
    ("Laboratorio", "Diagnóstico"),
]

MEDICAL_CENTERS = [
    ("Hospital Central", "Hospital", "Ciudad Autónoma de Buenos Aires", "CABA"),
    ("Centro Médico Norte", "Centro médico", "Vicente López", "Buenos Aires"),
    ("Centro Médico Sur", "Centro médico", "Avellaneda", "Buenos Aires"),
    ("Sede Belgrano", "Sede ambulatoria", "Ciudad Autónoma de Buenos Aires", "CABA"),
    ("Sede Caballito", "Sede ambulatoria", "Ciudad Autónoma de Buenos Aires", "CABA"),
]

INSURANCE_PLANS = [
    ("OSDE", "Plan 210", "Prepaga"),
    ("OSDE", "Plan 310", "Prepaga"),
    ("Swiss Medical", "SMG20", "Prepaga"),
    ("Galeno", "Oro", "Prepaga"),
    ("Medicus", "Azul", "Prepaga"),
    ("PAMI", "Plan único", "Obra social"),
    ("Particular", "Sin cobertura", "Particular"),
]


def truncate_reference_tables(connection) -> None:
    connection.execute(text("DELETE FROM dbo.billing"))
    connection.execute(text("DELETE FROM dbo.procedures"))
    connection.execute(text("DELETE FROM dbo.appointments"))
    connection.execute(text("DELETE FROM dbo.doctors"))
    connection.execute(text("DELETE FROM dbo.patients"))
    connection.execute(text("DELETE FROM dbo.insurance_plans"))
    connection.execute(text("DELETE FROM dbo.medical_centers"))
    connection.execute(text("DELETE FROM dbo.specialties"))

    connection.execute(text("DBCC CHECKIDENT ('dbo.billing', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.procedures', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.appointments', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.doctors', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.patients', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.insurance_plans', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.medical_centers', RESEED, 0)"))
    connection.execute(text("DBCC CHECKIDENT ('dbo.specialties', RESEED, 0)"))


def insert_specialties(connection) -> None:
    query = text("""
        INSERT INTO dbo.specialties (
            specialty_name,
            specialty_group
        )
        VALUES (
            :specialty_name,
            :specialty_group
        )
    """)

    rows = [
        {
            "specialty_name": specialty_name,
            "specialty_group": specialty_group,
        }
        for specialty_name, specialty_group in SPECIALTIES
    ]

    connection.execute(query, rows)


def insert_medical_centers(connection) -> None:
    query = text("""
        INSERT INTO dbo.medical_centers (
            center_name,
            center_type,
            city,
            province
        )
        VALUES (
            :center_name,
            :center_type,
            :city,
            :province
        )
    """)

    rows = [
        {
            "center_name": center_name,
            "center_type": center_type,
            "city": city,
            "province": province,
        }
        for center_name, center_type, city, province in MEDICAL_CENTERS
    ]

    connection.execute(query, rows)


def insert_insurance_plans(connection) -> None:
    query = text("""
        INSERT INTO dbo.insurance_plans (
            insurance_name,
            plan_name,
            plan_type
        )
        VALUES (
            :insurance_name,
            :plan_name,
            :plan_type
        )
    """)

    rows = [
        {
            "insurance_name": insurance_name,
            "plan_name": plan_name,
            "plan_type": plan_type,
        }
        for insurance_name, plan_name, plan_type in INSURANCE_PLANS
    ]

    connection.execute(query, rows)


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        truncate_reference_tables(connection)
        insert_specialties(connection)
        insert_medical_centers(connection)
        insert_insurance_plans(connection)

    print("Datos de referencia cargados correctamente.")
    print(f"Especialidades cargadas: {len(SPECIALTIES)}")
    print(f"Sedes cargadas: {len(MEDICAL_CENTERS)}")
    print(f"Coberturas cargadas: {len(INSURANCE_PLANS)}")


if __name__ == "__main__":
    main()