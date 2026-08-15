import random
from datetime import datetime, timedelta

from sqlalchemy import text

from data_generator.database import get_engine


random.seed(2026)

PROCEDURE_CATALOG = [
    ("CONS001", "Consulta médica", 12000.00),
    ("CONS002", "Consulta especialista", 18000.00),
    ("LAB001", "Hemograma completo", 6500.00),
    ("LAB002", "Glucemia", 3500.00),
    ("LAB003", "Perfil lipídico", 8000.00),
    ("IMG001", "Radiografía", 15000.00),
    ("IMG002", "Ecografía", 22000.00),
    ("IMG003", "Tomografía", 65000.00),
    ("CARD001", "Electrocardiograma", 10000.00),
    ("CARD002", "Ecocardiograma", 35000.00),
    ("TRAU001", "Inmovilización", 18000.00),
    ("OFT001", "Fondo de ojo", 14000.00),
]


def get_completed_appointments(connection) -> list[dict]:
    result = connection.execute(
        text("""
            SELECT
                appointment_id,
                patient_id,
                doctor_id,
                specialty_id,
                medical_center_id,
                insurance_plan_id,
                appointment_datetime
            FROM dbo.appointments
            WHERE status = 'completed'
        """)
    )

    return [
        {
            "appointment_id": row.appointment_id,
            "patient_id": row.patient_id,
            "doctor_id": row.doctor_id,
            "specialty_id": row.specialty_id,
            "medical_center_id": row.medical_center_id,
            "insurance_plan_id": row.insurance_plan_id,
            "appointment_datetime": row.appointment_datetime,
        }
        for row in result
    ]


def generate_procedures_for_appointment(appointment: dict) -> list[dict]:
    procedures = []

    # La mayoría de los turnos tiene 1 prestación; algunos tienen 2 o 3.
    procedure_count = random.choices(
        [1, 2, 3],
        weights=[80, 17, 3],
        k=1
    )[0]

    selected_procedures = random.sample(PROCEDURE_CATALOG, k=procedure_count)

    now = datetime.now()

    for procedure_code, procedure_name, unit_price in selected_procedures:
        procedure_datetime = appointment["appointment_datetime"] + timedelta(
            minutes=random.randint(0, 90)
        )

        procedures.append({
            "patient_id": appointment["patient_id"],
            "doctor_id": appointment["doctor_id"],
            "specialty_id": appointment["specialty_id"],
            "medical_center_id": appointment["medical_center_id"],
            "insurance_plan_id": appointment["insurance_plan_id"],
            "appointment_id": appointment["appointment_id"],
            "procedure_code": procedure_code,
            "procedure_name": procedure_name,
            "procedure_datetime": procedure_datetime,
            "quantity": 1,
            "unit_price": unit_price,
            "created_at": now,
            "updated_at": now,
        })

    return procedures


def insert_procedures(connection, procedures: list[dict]) -> None:
    query = text("""
        INSERT INTO dbo.procedures (
            patient_id,
            doctor_id,
            specialty_id,
            medical_center_id,
            insurance_plan_id,
            appointment_id,
            procedure_code,
            procedure_name,
            procedure_datetime,
            quantity,
            unit_price,
            created_at,
            updated_at
        )
        VALUES (
            :patient_id,
            :doctor_id,
            :specialty_id,
            :medical_center_id,
            :insurance_plan_id,
            :appointment_id,
            :procedure_code,
            :procedure_name,
            :procedure_datetime,
            :quantity,
            :unit_price,
            :created_at,
            :updated_at
        )
    """)

    connection.execute(query, procedures)


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        completed_appointments = get_completed_appointments(connection)

        if not completed_appointments:
            raise ValueError("No hay turnos completed para generar prestaciones.")

        print(f"Turnos completed encontrados: {len(completed_appointments)}")
        print("Generando prestaciones...")

        procedures = []

        for appointment in completed_appointments:
            procedures.extend(generate_procedures_for_appointment(appointment))

        insert_procedures(connection, procedures)

    print(f"Prestaciones cargadas correctamente: {len(procedures)}")


if __name__ == "__main__":
    main()