# GKCCF Internal Request Tracker

Initial full-stack skeleton for the GKCCF Internal Request Tracker MVP described in `docs/PRD.md`.

## Stack

- Backend: Django, Django REST Framework, django-cors-headers, SQLite
- Frontend: React + Vite (JavaScript)

## Project Structure

- `backend/` Django project and app scaffold
- `frontend/` React + Vite scaffold
- `docs/` product requirements and related documentation

## Backend Setup

From the repository root:

```powershell
python -m pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py runserver
```

Backend will run at `http://127.0.0.1:8000/`.

## Frontend Setup

Open a second terminal from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend will run at `http://127.0.0.1:5173/`.

## Local Development Notes

- SQLite is configured by default for quick local setup.
- CORS is enabled for common local React dev origins:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`
  - `http://localhost:3000`
  - `http://127.0.0.1:3000`
- `requests_app` has been created, but no PRD business models or request APIs are implemented yet.

## Quick Verification

- Backend: visit `http://127.0.0.1:8000/` and confirm the plain text backend message appears.
- Frontend: visit `http://127.0.0.1:5173/` and confirm the starter page for the GKCCF app loads.
