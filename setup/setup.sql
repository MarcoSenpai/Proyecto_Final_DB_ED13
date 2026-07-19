%sql

-- 1. Crear catalog
CREATE CATALOG IF NOT EXISTS proyecto_final;

-- 2. Crear schemas
CREATE SCHEMA IF NOT EXISTS proyecto_final.landing;
CREATE SCHEMA IF NOT EXISTS proyecto_final.bronze;
CREATE SCHEMA IF NOT EXISTS proyecto_final.silver;
CREATE SCHEMA IF NOT EXISTS proyecto_final.gold;

-- 3. Crear volume
CREATE VOLUME IF NOT EXISTS proyecto_final.landing.raw_data;