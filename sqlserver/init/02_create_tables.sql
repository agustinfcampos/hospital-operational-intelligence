USE hospital_oltp;
GO

IF OBJECT_ID('dbo.billing', 'U') IS NOT NULL DROP TABLE dbo.billing;
IF OBJECT_ID('dbo.procedures', 'U') IS NOT NULL DROP TABLE dbo.procedures;
IF OBJECT_ID('dbo.appointments', 'U') IS NOT NULL DROP TABLE dbo.appointments;
IF OBJECT_ID('dbo.doctors', 'U') IS NOT NULL DROP TABLE dbo.doctors;
IF OBJECT_ID('dbo.patients', 'U') IS NOT NULL DROP TABLE dbo.patients;
IF OBJECT_ID('dbo.insurance_plans', 'U') IS NOT NULL DROP TABLE dbo.insurance_plans;
IF OBJECT_ID('dbo.medical_centers', 'U') IS NOT NULL DROP TABLE dbo.medical_centers;
IF OBJECT_ID('dbo.specialties', 'U') IS NOT NULL DROP TABLE dbo.specialties;
GO

CREATE TABLE dbo.specialties (
    specialty_id INT IDENTITY(1,1) PRIMARY KEY,
    specialty_name VARCHAR(100) NOT NULL,
    specialty_group VARCHAR(100) NOT NULL,
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.medical_centers (
    medical_center_id INT IDENTITY(1,1) PRIMARY KEY,
    center_name VARCHAR(150) NOT NULL,
    center_type VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.insurance_plans (
    insurance_plan_id INT IDENTITY(1,1) PRIMARY KEY,
    insurance_name VARCHAR(100) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(50) NOT NULL,
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.patients (
    patient_id INT IDENTITY(1,1) PRIMARY KEY,
    document_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(150) NULL,
    phone VARCHAR(50) NULL,
    city VARCHAR(100) NULL,
    province VARCHAR(100) NULL,
    insurance_plan_id INT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_patients_insurance_plans
        FOREIGN KEY (insurance_plan_id)
        REFERENCES dbo.insurance_plans (insurance_plan_id)
);
GO

CREATE TABLE dbo.doctors (
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    specialty_id INT NOT NULL,
    medical_center_id INT NOT NULL,
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_doctors_specialties
        FOREIGN KEY (specialty_id)
        REFERENCES dbo.specialties (specialty_id),

    CONSTRAINT FK_doctors_medical_centers
        FOREIGN KEY (medical_center_id)
        REFERENCES dbo.medical_centers (medical_center_id)
);
GO

CREATE TABLE dbo.appointments (
    appointment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    specialty_id INT NOT NULL,
    medical_center_id INT NOT NULL,
    insurance_plan_id INT NOT NULL,
    appointment_datetime DATETIME2 NOT NULL,
    status VARCHAR(30) NOT NULL,
    scheduled_at DATETIME2 NOT NULL,
    cancelled_at DATETIME2 NULL,
    cancellation_reason VARCHAR(200) NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_appointments_patients
        FOREIGN KEY (patient_id)
        REFERENCES dbo.patients (patient_id),

    CONSTRAINT FK_appointments_doctors
        FOREIGN KEY (doctor_id)
        REFERENCES dbo.doctors (doctor_id),

    CONSTRAINT FK_appointments_specialties
        FOREIGN KEY (specialty_id)
        REFERENCES dbo.specialties (specialty_id),

    CONSTRAINT FK_appointments_medical_centers
        FOREIGN KEY (medical_center_id)
        REFERENCES dbo.medical_centers (medical_center_id),

    CONSTRAINT FK_appointments_insurance_plans
        FOREIGN KEY (insurance_plan_id)
        REFERENCES dbo.insurance_plans (insurance_plan_id),

    CONSTRAINT CK_appointments_status
        CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show', 'rescheduled'))
);
GO

CREATE TABLE dbo.procedures (
    procedure_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    specialty_id INT NOT NULL,
    medical_center_id INT NOT NULL,
    insurance_plan_id INT NOT NULL,
    appointment_id INT NULL,
    procedure_code VARCHAR(50) NOT NULL,
    procedure_name VARCHAR(200) NOT NULL,
    procedure_datetime DATETIME2 NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(18,2) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_procedures_patients
        FOREIGN KEY (patient_id)
        REFERENCES dbo.patients (patient_id),

    CONSTRAINT FK_procedures_doctors
        FOREIGN KEY (doctor_id)
        REFERENCES dbo.doctors (doctor_id),

    CONSTRAINT FK_procedures_specialties
        FOREIGN KEY (specialty_id)
        REFERENCES dbo.specialties (specialty_id),

    CONSTRAINT FK_procedures_medical_centers
        FOREIGN KEY (medical_center_id)
        REFERENCES dbo.medical_centers (medical_center_id),

    CONSTRAINT FK_procedures_insurance_plans
        FOREIGN KEY (insurance_plan_id)
        REFERENCES dbo.insurance_plans (insurance_plan_id),

    CONSTRAINT FK_procedures_appointments
        FOREIGN KEY (appointment_id)
        REFERENCES dbo.appointments (appointment_id)
);
GO

CREATE TABLE dbo.billing (
    billing_id INT IDENTITY(1,1) PRIMARY KEY,
    procedure_id INT NOT NULL,
    patient_id INT NOT NULL,
    insurance_plan_id INT NOT NULL,
    medical_center_id INT NOT NULL,
    billing_date DATE NOT NULL,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    billing_status VARCHAR(30) NOT NULL,
    gross_amount DECIMAL(18,2) NOT NULL,
    discount_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    net_amount DECIMAL(18,2) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_billing_procedures
        FOREIGN KEY (procedure_id)
        REFERENCES dbo.procedures (procedure_id),

    CONSTRAINT FK_billing_patients
        FOREIGN KEY (patient_id)
        REFERENCES dbo.patients (patient_id),

    CONSTRAINT FK_billing_insurance_plans
        FOREIGN KEY (insurance_plan_id)
        REFERENCES dbo.insurance_plans (insurance_plan_id),

    CONSTRAINT FK_billing_medical_centers
        FOREIGN KEY (medical_center_id)
        REFERENCES dbo.medical_centers (medical_center_id),

    CONSTRAINT CK_billing_status
        CHECK (billing_status IN ('pending', 'approved', 'rejected', 'paid', 'cancelled'))
);
GO