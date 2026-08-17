-- 01. Preview de pacientes
SELECT *
FROM patients
LIMIT 10;


-- 02. Distribución de pacientes por género
SELECT
    gender,
    COUNT(*) AS total_patients
FROM patients
GROUP BY gender
ORDER BY total_patients DESC;


-- 03. Turnos por estado
SELECT
    status,
    COUNT(*) AS total_appointments
FROM appointments
GROUP BY status
ORDER BY total_appointments DESC;


-- 04. Facturación por estado
SELECT 
    billing_status,
    COUNT(*) AS total_billing_records,
    SUM(net_amount) AS total_net_amount
FROM billing
GROUP BY billing_status
ORDER BY total_net_amount DESC;


-- 05. Turnos por especialidad, sede y estado
SELECT
    s.specialty_name,
    mc.center_name,
    a.status,
    COUNT(*) AS total_appointments
FROM appointments a
JOIN doctors d
    ON a.doctor_id = d.doctor_id
JOIN specialties s
    ON d.specialty_id = s.specialty_id
JOIN medical_centers mc
    ON a.medical_center_id = mc.medical_center_id
GROUP BY
    s.specialty_name,
    mc.center_name,
    a.status
ORDER BY
    total_appointments DESC
LIMIT 20;