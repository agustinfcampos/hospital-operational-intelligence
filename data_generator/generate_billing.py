import random
from datetime import datetime, timedelta

from sqlalchemy import text

from data_generator.database import get_engine


random.seed(2026)

BILLING_STATUSES = ["pending", "approved", "rejected", "paid", "cancelled"]
BILLING_STATUS_WEIGHTS = [10, 25, 8, 52, 5]


def get_procedures(connection) -> list[dict]:
    result = connection.execute(
        text("""
            SELECT
                procedure_id,
                patient_id,
                insurance_plan_id,
                medical_center_id,
                procedure_datetime,
                quantity,
                unit_price
            FROM dbo.procedures
        """)
    )

    return [
        {
            "procedure_id": row.procedure_id,
            "patient_id": row.patient_id,
            "insurance_plan_id": row.insurance_plan_id,
            "medical_center_id": row.medical_center_id,
            "procedure_datetime": row.procedure_datetime,
            "quantity": row.quantity,
            "unit_price": row.unit_price,
        }
        for row in result
    ]


def generate_invoice_number(index: int) -> str:
    return f"FAC-{2026}-{index:08d}"


def generate_billing_row(index: int, procedure: dict) -> dict:
    gross_amount = float(procedure["quantity"]) * float(procedure["unit_price"])

    discount_percentage = random.choices(
        [0, 5, 10, 15, 20],
        weights=[65, 15, 10, 7, 3],
        k=1
    )[0]

    discount_amount = round(gross_amount * discount_percentage / 100, 2)
    net_amount = round(gross_amount - discount_amount, 2)

    billing_status = random.choices(
        BILLING_STATUSES,
        weights=BILLING_STATUS_WEIGHTS,
        k=1
    )[0]

    billing_date = procedure["procedure_datetime"].date() + timedelta(
        days=random.randint(0, 20)
    )

    now = datetime.now()

    return {
        "procedure_id": procedure["procedure_id"],
        "patient_id": procedure["patient_id"],
        "insurance_plan_id": procedure["insurance_plan_id"],
        "medical_center_id": procedure["medical_center_id"],
        "billing_date": billing_date,
        "invoice_number": generate_invoice_number(index),
        "billing_status": billing_status,
        "gross_amount": gross_amount,
        "discount_amount": discount_amount,
        "net_amount": net_amount,
        "created_at": now,
        "updated_at": now,
    }


def insert_billing(connection, billing_rows: list[dict]) -> None:
    query = text("""
        INSERT INTO dbo.billing (
            procedure_id,
            patient_id,
            insurance_plan_id,
            medical_center_id,
            billing_date,
            invoice_number,
            billing_status,
            gross_amount,
            discount_amount,
            net_amount,
            created_at,
            updated_at
        )
        VALUES (
            :procedure_id,
            :patient_id,
            :insurance_plan_id,
            :medical_center_id,
            :billing_date,
            :invoice_number,
            :billing_status,
            :gross_amount,
            :discount_amount,
            :net_amount,
            :created_at,
            :updated_at
        )
    """)

    connection.execute(query, billing_rows)


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        procedures = get_procedures(connection)

        if not procedures:
            raise ValueError("No hay prestaciones cargadas en dbo.procedures")

        print(f"Prestaciones encontradas: {len(procedures)}")
        print("Generando facturación...")

        billing_rows = [
            generate_billing_row(index, procedure)
            for index, procedure in enumerate(procedures, start=1)
        ]

        insert_billing(connection, billing_rows)

    print(f"Registros de facturación cargados correctamente: {len(billing_rows)}")


if __name__ == "__main__":
    main()