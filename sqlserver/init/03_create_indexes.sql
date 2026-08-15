USE hospital_oltp;
GO

CREATE INDEX IX_patients_insurance_plan_id
ON dbo.patients (insurance_plan_id);
GO

CREATE INDEX IX_doctors_specialty_id
ON dbo.doctors (specialty_id);
GO

CREATE INDEX IX_doctors_medical_center_id
ON dbo.doctors (medical_center_id);
GO

CREATE INDEX IX_appointments_patient_id
ON dbo.appointments (patient_id);
GO

CREATE INDEX IX_appointments_doctor_id
ON dbo.appointments (doctor_id);
GO

CREATE INDEX IX_appointments_specialty_id
ON dbo.appointments (specialty_id);
GO

CREATE INDEX IX_appointments_medical_center_id
ON dbo.appointments (medical_center_id);
GO

CREATE INDEX IX_appointments_insurance_plan_id
ON dbo.appointments (insurance_plan_id);
GO

CREATE INDEX IX_appointments_datetime
ON dbo.appointments (appointment_datetime);
GO

CREATE INDEX IX_appointments_status
ON dbo.appointments (status);
GO

CREATE INDEX IX_procedures_patient_id
ON dbo.procedures (patient_id);
GO

CREATE INDEX IX_procedures_doctor_id
ON dbo.procedures (doctor_id);
GO

CREATE INDEX IX_procedures_specialty_id
ON dbo.procedures (specialty_id);
GO

CREATE INDEX IX_procedures_medical_center_id
ON dbo.procedures (medical_center_id);
GO

CREATE INDEX IX_procedures_insurance_plan_id
ON dbo.procedures (insurance_plan_id);
GO

CREATE INDEX IX_procedures_appointment_id
ON dbo.procedures (appointment_id);
GO

CREATE INDEX IX_procedures_datetime
ON dbo.procedures (procedure_datetime);
GO

CREATE INDEX IX_billing_procedure_id
ON dbo.billing (procedure_id);
GO

CREATE INDEX IX_billing_patient_id
ON dbo.billing (patient_id);
GO

CREATE INDEX IX_billing_insurance_plan_id
ON dbo.billing (insurance_plan_id);
GO

CREATE INDEX IX_billing_medical_center_id
ON dbo.billing (medical_center_id);
GO

CREATE INDEX IX_billing_date
ON dbo.billing (billing_date);
GO

CREATE INDEX IX_billing_status
ON dbo.billing (billing_status);
GO