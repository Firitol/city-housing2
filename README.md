# Hosana City Housing Management System

A professional governmental web system for **Hosana City** to manage householder profiles by house number. The platform supports mayor and staff access with secure registration/login, searchable records, profile editing, and CSV upload.

## Core Features

- Role-based staff account registration and login (`mayor`, `staff`).
- Search householders by **house number** or **name**.
- Create and update householder profiles.
- CSV upload for bulk householder data import.
- Administrative structure support for:
  - **3 menders** (`Mender 1-3`)
  - **10 kebeles** (`Kebele 1-10`)
- Production-ready deployment configuration for **Render**.
- PostgreSQL-ready database connection.
- Public icon and clean professional interface.

## Technology Stack

- Python + Flask
- Flask-Login for authentication
- Flask-SQLAlchemy + Flask-Migrate for data layer
- PostgreSQL (`psycopg2-binary`)
- Gunicorn for production serving
- Bootstrap for UI styling

## Local Installation

1. Clone repository and enter the project.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables (`.env`):

```bash
SECRET_KEY=replace-with-strong-secret
DATABASE_URL=postgresql://username:password@localhost:5432/hosana_city_housing
```

> For quick local testing only, if `DATABASE_URL` is not set it will fallback to SQLite (`hosana_city_housing.db`).

5. Run the app:

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

## CSV Upload Format

Use headers:

```csv
house_number,first_name,last_name,phone,mender,kebele,family_size,notes
```

Only valid rows are imported (unique house number + valid mender/kebele values).


## Neon Database Table Creation

If you want to create tables directly on a Neon PostgreSQL database, run:

```bash
psql "$DATABASE_URL" -f db/schema_neon.sql
```

The script creates:
- `users`
- `householders`
- indexes for search fields
- an update trigger for `updated_at`

## Render Deployment

This repository includes:

- `render.yaml` (web service + managed PostgreSQL database)
- `Procfile` (`gunicorn wsgi:app`)

### Deploy steps

1. Push this repo to GitHub.
2. In Render, create a **Blueprint** deployment from the repo.
3. Render provisions:
   - web service: `hosana-city-housing`
   - PostgreSQL database: `hosana-city-housing-db`
4. Ensure migrations/tables are created on first run.

## Default Roles

During registration choose:

- **Mayor** for city-level access.
- **Staff Worker** for official operations.

## Project Structure

```text
app/
  __init__.py
  auth.py
  models.py
  routes.py
  templates/
  static/
app.py
requirements.txt
Procfile
render.yaml
```
