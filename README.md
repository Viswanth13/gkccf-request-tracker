# GKCCF Internal Request Tracker MVP

## Overview

GKCCF Internal Request Tracker is a full-stack MVP for managing internal donor and advisor service requests. It gives staff a lightweight internal dashboard to review requests, track status, capture internal notes, and generate a mock AI-assisted response draft that still requires human review before anything is sent.

## Why This App Exists

GKCCF teams often need a simple way to manage grant help requests, fund questions, advisor needs, and related internal workflows without relying on a generic ticketing tool. This MVP demonstrates a focused internal workflow with realistic service request data, clear request visibility, and a safe review-first AI draft experience.

## Tech Stack

- Backend: Django, Django REST Framework, django-cors-headers
- Database: SQLite for local MVP development
- Frontend: React, Vite, JavaScript
- Styling: Plain CSS
- Testing:
  - Backend: Django `TestCase` and DRF `APITestCase`
  - Frontend: Vitest, React Testing Library, `@testing-library/jest-dom`, jsdom

## Features Implemented

- Read-only service request list API
- Request detail API with owner, notes, status history, and latest AI draft
- Workflow APIs for:
  - adding an internal note
  - updating request status
  - generating a mock AI draft response
- Demo seed data command with idempotent behavior
- Internal dashboard UI with:
  - sidebar and topbar
  - metric cards
  - category filters
  - searchable request table
  - right-side request detail drawer
  - status update action
  - internal note action
  - mock AI draft generation action
- Backend and frontend test coverage for core MVP behavior

## Repository Structure

```text
gkccf-request-tracker/
├── backend/
├── frontend/
└── docs/
```

## Local Setup (Windows PowerShell)

### Backend Setup

```powershell
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Backend runs at:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Frontend Setup

Open a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs at:

- [http://127.0.0.1:5173/](http://127.0.0.1:5173/)

## Useful Commands

### Seed Demo Data

```powershell
cd backend
python manage.py seed_demo_data
```

### Run Backend Tests

```powershell
cd backend
python manage.py test requests_app
```

### Run Frontend Tests

```powershell
cd frontend
npm test
```

### Build Frontend

```powershell
cd frontend
npm run build
```

## API Endpoints

### Read APIs

- `GET /api/requests/`
- `GET /api/requests/<id>/`

### Workflow APIs

- `POST /api/requests/<id>/notes/`
- `PATCH /api/requests/<id>/status/`
- `POST /api/requests/<id>/generate-draft/`

## Mock User

The current frontend workflow uses this mock staff user for demo actions:

- `Sarah Kim` — `Donor Services`

Demo seed data also includes:

- `Michael Lee` — `Donor Services`
- `Alicia Brown` — `Grants Operations`
- `David Patel` — `Advisor Services`

## Demo Flow

1. Start the backend and frontend.
2. Open the Service Requests dashboard in the browser.
3. Scan the metric cards and request table.
4. Use search or category filters to narrow the list.
5. Click a request row to open the right-side detail drawer.
6. Review request details, missing information, notes, and status history.
7. Add an internal note as Sarah Kim.
8. Update the request status.
9. Generate a mock AI draft response.
10. Explain that the draft is review-only and must be checked by a human before use.

## Known Limitations

- No authentication or role-based access control yet
- No real email sending
- No real AI provider integration
- No production deployment configuration yet
- SQLite is used for local MVP simplicity
- Sidebar items other than `Requests` are visual only
- Frontend search and category filtering are handled client-side
- No file uploads, attachments, or audit export features yet
- The AI draft is deterministic mock content, not a live model response

## Future Improvements

- Add authentication and internal staff permissions
- Move from SQLite to PostgreSQL
- Add richer filtering, sorting, and pagination
- Add real notification flows
- Add file attachments and supporting documents
- Add request assignment workflows
- Add analytics and reporting views
- Integrate a real AI drafting workflow with approval controls
- Add deployment configuration for staging and production

## Source Of Truth

Product requirements live in:

- [docs/PRD.md](C:\Users\VISWANTH\Desktop\Placement\US\GKCCF\GKCCF_MVP\gkccf-request-tracker\docs\PRD.md)

For a guided presentation outline, see:

- [docs/demo-script.md](C:\Users\VISWANTH\Desktop\Placement\US\GKCCF\GKCCF_MVP\gkccf-request-tracker\docs\demo-script.md)
