IF DB_ID('hospital_oltp') IS NULL
BEGIN
    CREATE DATABASE hospital_oltp;
END;
GO