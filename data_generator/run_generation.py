from data_generator.generate_reference_data import main as generate_reference_data
from data_generator.generate_patients import main as generate_patients
from data_generator.generate_doctors import main as generate_doctors
from data_generator.generate_appointments import main as generate_appointments
from data_generator.generate_procedures import main as generate_procedures
from data_generator.generate_billing import main as generate_billing


def main() -> None:
    print("Iniciando generación completa de datos OLTP hospitalarios...")

    print("\n1. Cargando datos de referencia...")
    generate_reference_data()

    print("\n2. Generando pacientes...")
    generate_patients()

    print("\n3. Generando médicos...")
    generate_doctors()

    print("\n4. Generando turnos...")
    generate_appointments()

    print("\n5. Generando prestaciones...")
    generate_procedures()

    print("\n6. Generando facturación...")
    generate_billing()

    print("\nProceso completo finalizado correctamente.")


if __name__ == "__main__":
    main()