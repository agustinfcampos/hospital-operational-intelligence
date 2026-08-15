import random
from datetime import datetime

from faker import Faker
from sqlalchemy import text

from data_generator.database import get_engine


fake = Faker("es_AR")
Faker.seed(2026)
random.seed(2026)


PATIENTS_TO_GENERATE = 5000

GENDERS = ["female", "male", "other"]


def get_insurance_plan_ids(connection) -> list[int]:
    result = connection.execute(
        text("SELECT insurance_plan_id FROM dbo.insurance_plans WHERE active = 1")
    )
    return [row.insurance_plan_id for row in result]


def generate_document_number(index: int) -> str:
    return str(20000000 + index)


def generate_patient(index: int, insurance_plan_ids: list[int]) -> dict:
    gender = random.choices(
        GENDERS,
        weights=[49, 49, 2],
        k=1
    )[0]

    if gender == "female":
        first_name = fake.first_name_female()
    elif gender == "male":
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name()

    last_name = fake.last_name()

    birth_date = fake.date_of_birth(
        minimum_age=0,
        maximum_age=95
    )

    now = datetime.now()

    return {
        "document_number": generate_document_number(index),
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "birth_date": birth_date,
        "email": fake.email().lower(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "province": fake.province(),
        "insurance_plan_id": random.choice(insurance_plan_ids),
        "created_at": now,
        "updated_at": now,
    }


def insert_patients(connection, patients: list[dict]) -> None:
    query = text("""
        INSERT INTO dbo.patients (
            document_number,
            first_name,
            last_name,
            gender,
            birth_date,
            email,
            phone,
            city,
            province,
            insurance_plan_id,
            created_at,
            updated_at
        )
        VALUES (
            :document_number,
            :first_name,
            :last_name,
            :gender,
            :birth_date,
            :email,
            :phone,
            :city,
            :province,
            :insurance_plan_id,
            :created_at,
            :updated_at
        )
    """)

    connection.execute(query, patients)


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        insurance_plan_ids = get_insurance_plan_ids(connection)

        if not insurance_plan_ids:
            raise ValueError("No hay coberturas cargadas en dbo.insurance_plans")

        print(f"Generando {PATIENTS_TO_GENERATE} pacientes...")

        patients = [
            generate_patient(index, insurance_plan_ids)
            for index in range(1, PATIENTS_TO_GENERATE + 1)
        ]

        insert_patients(connection, patients)

    print("Pacientes cargados correctamente.")


if __name__ == "__main__":
    main()