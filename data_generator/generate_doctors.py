import random
from datetime import datetime

from faker import Faker
from sqlalchemy import text

from data_generator.database import get_engine


fake = Faker("es_AR")
Faker.seed(2026)
random.seed(2026)


DOCTORS_TO_GENERATE = 250


def get_specialty_ids(connection) -> list[int]:
    result = connection.execute(
        text("SELECT specialty_id FROM dbo.specialties WHERE active = 1")
    )
    return [row.specialty_id for row in result]


def get_medical_center_ids(connection) -> list[int]:
    result = connection.execute(
        text("SELECT medical_center_id FROM dbo.medical_centers WHERE active = 1")
    )
    return [row.medical_center_id for row in result]


def generate_license_number(index: int) -> str:
    return f"MN-{100000 + index}"


def generate_doctor(
    index: int,
    specialty_ids: list[int],
    medical_center_ids: list[int],
) -> dict:
    now = datetime.now()

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "license_number": generate_license_number(index),
        "specialty_id": random.choice(specialty_ids),
        "medical_center_id": random.choice(medical_center_ids),
        "active": True,
        "created_at": now,
        "updated_at": now,
    }


def insert_doctors(connection, doctors: list[dict]) -> None:
    query = text("""
        INSERT INTO dbo.doctors (
            first_name,
            last_name,
            license_number,
            specialty_id,
            medical_center_id,
            active,
            created_at,
            updated_at
        )
        VALUES (
            :first_name,
            :last_name,
            :license_number,
            :specialty_id,
            :medical_center_id,
            :active,
            :created_at,
            :updated_at
        )
    """)

    connection.execute(query, doctors)


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        specialty_ids = get_specialty_ids(connection)
        medical_center_ids = get_medical_center_ids(connection)

        if not specialty_ids:
            raise ValueError("No hay especialidades cargadas en dbo.specialties")

        if not medical_center_ids:
            raise ValueError("No hay sedes cargadas en dbo.medical_centers")

        print(f"Generando {DOCTORS_TO_GENERATE} médicos...")

        doctors = [
            generate_doctor(index, specialty_ids, medical_center_ids)
            for index in range(1, DOCTORS_TO_GENERATE + 1)
        ]

        insert_doctors(connection, doctors)

    print("Médicos cargados correctamente.")


if __name__ == "__main__":
    main()