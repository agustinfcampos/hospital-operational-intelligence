import random
from datetime import datetime, timedelta, time

from sqlalchemy import text

from data_generator.database import get_engine


random.seed(2026)

APPOINTMENTS_TO_GENERATE = 30000

STATUSES = ["scheduled", "completed", "cancelled", "no_show", "rescheduled"]
STATUS_WEIGHTS = [15, 60, 12, 8, 5]

CANCELLATION_REASONS = [
    "patient_request",
    "doctor_unavailable",
    "administrative_error",
    "insurance_issue",
    "weather_conditions",
    "unknown",
]


def get_patients(connection) -> list[dict]:
    result = connection.execute(
        text("""
            SELECT patient_id, insurance_plan_id
            FROM dbo.patients
        """)
    )

    return [
        {
            "patient_id": row.patient_id,
            "insurance_plan_id": row.insurance_plan_id,
        }
        for row in result
    ]


def get_doctors(connection) -> list[dict]:
    result = connection.execute(
        text("""
            SELECT doctor_id, specialty_id, medical_center_id
            FROM dbo.doctors
            WHERE active = 1
        """)
    )

    return [
        {
            "doctor_id": row.doctor_id,
            "specialty_id": row.specialty_id,
            "medical_center_id": row.medical_center_id,
        }
        for row in result
    ]


def random_appointment_datetime() -> datetime:
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 365)

    appointment_date = start_date + timedelta(days=random_days)

    possible_hours = list(range(8, 19))
    possible_minutes = [0, 15, 30, 45]

    return datetime.combine(
        appointment_date.date(),
        time(
            hour=random.choice(possible_hours),
            minute=random.choice(possible_minutes),
        )
    )


def generate_appointment(
    patients: list[dict],
    doctors: list[dict],
) -> dict:
    patient = random.choice(patients)
    doctor = random.choice(doctors)

    appointment_datetime = random_appointment_datetime()
    scheduled_at = appointment_datetime - timedelta(days=random.randint(1, 90))

    status = random.choices(
        STATUSES,
        weights=STATUS_WEIGHTS,
        k=1
    )[0]

    cancelled_at = None
    cancellation_reason = None

    if status == "cancelled":
        cancelled_at = appointment_datetime - timedelta(
            days=random.randint(0, 10),
            hours=random.randint(0, 23)
        )
        cancellation_reason = random.choice(CANCELLATION_REASONS)

    now = datetime.now()

    return {
        "patient_id": patient["patient_id"],
        "doctor_id": doctor["doctor_id"],
        "specialty_id": doctor["specialty_id"],
        "medical_center_id": doctor["medical_center_id"],
        "insurance_plan_id": patient["insurance_plan_id"],
        "appointment_datetime": appointment_datetime,
        "status": status,
        "scheduled_at": scheduled_at,
        "cancelled_at": cancelled_at,
        "cancellation_reason": cancellation_reason,
        "created_at": now,
        "updated_at": now,
    }


def insert_appointments(connection, appointments: list[dict]) -> None:
    query = text("""
        INSERT INTO dbo.appointments (
            patient_id,
            doctor_id,
            specialty_id,
            medical_center_id,
            insurance_plan_id,
            appointment_datetime,
            status,
            scheduled_at,
            cancelled_at,
            cancellation_reason,
            created_at,
            updated_at
        )
        VALUES (
            :patient_id,
            :doctor_id,
            :specialty_id,
            :medical_center_id,
            :insurance_plan_id,
            :appointment_datetime,
            :status,
            :scheduled_at,
            :cancelled_at,
            :cancellation_reason,
            :created_at,
            :updated_at
        )
    """)

    connection.execute(query, appointments)


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        patients = get_patients(connection)
        doctors = get_doctors(connection)

        if not patients:
            raise ValueError("No hay pacientes cargados en dbo.patients")

        if not doctors:
            raise ValueError("No hay médicos cargados en dbo.doctors")

        print(f"Generando {APPOINTMENTS_TO_GENERATE} turnos...")

        appointments = [
            generate_appointment(patients, doctors)
            for _ in range(APPOINTMENTS_TO_GENERATE)
        ]

        insert_appointments(connection, appointments)

    print("Turnos cargados correctamente.")


if __name__ == "__main__":
    main()