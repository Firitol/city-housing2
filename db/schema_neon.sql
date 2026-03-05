-- Hosana City Housing Management System
-- Neon/PostgreSQL table creation script
-- Run with: psql "$DATABASE_URL" -f db/schema_neon.sql

BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
    role VARCHAR(30) NOT NULL DEFAULT 'staff' CHECK (role IN ('mayor', 'staff')),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS householders (
    id BIGSERIAL PRIMARY KEY,
    house_number VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    phone VARCHAR(20),
    mender VARCHAR(40) NOT NULL CHECK (mender IN ('Mender 1', 'Mender 2', 'Mender 3')),
    kebele VARCHAR(40) NOT NULL CHECK (
        kebele IN (
            'Kebele 1', 'Kebele 2', 'Kebele 3', 'Kebele 4', 'Kebele 5',
            'Kebele 6', 'Kebele 7', 'Kebele 8', 'Kebele 9', 'Kebele 10'
        )
    ),
    family_size INTEGER NOT NULL DEFAULT 1 CHECK (family_size > 0),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_householders_house_number ON householders (house_number);
CREATE INDEX IF NOT EXISTS idx_householders_first_name ON householders (first_name);
CREATE INDEX IF NOT EXISTS idx_householders_last_name ON householders (last_name);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_householders_set_updated_at ON householders;
CREATE TRIGGER trg_householders_set_updated_at
BEFORE UPDATE ON householders
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

COMMIT;
