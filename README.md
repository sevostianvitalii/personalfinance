# Personal Finance Analyzer

A powerful, self-hosted personal finance application built with **FastAPI** (Backend) and **React** (Frontend).
Analyze your bank statements (PDF), categorize transactions, and visualize your spending habits.

## Features

- **PDF Statement Upload**: Drag & drop support for bank statements (e.g., Swedbank).
- **Auto-Categorization**: Smart keyword-based categorization for food, transport, utilities, etc.
- **Interactive Dashboard**:
    - **Periods**: View by Day, Week, Month, or Year.
    - **Date Ranges**: Pick precise start and end dates.
    - **Charts**: Interactive bar charts (Income/Expense) and pie charts (Category breakdown).
- **Advanced Filtering**:
    - Filter by **Category** (e.g., "Savings").
    - **Search** transactions by description or recipient.
- **Reporting**: Export analysis as PDF reports.
- **Privacy Focus**: All data stays local (SQLite).

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Pandas, PDFPlumber.
- **Frontend**: React, Vite, Recharts, Lucide React.
- **Database**: SQLite.

## How to Run

### Using Docker (Recommended)
You can run the entire application (Backend + Frontend) with a single command:

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000

Data (`finance.db` and `uploads/`) will be persisted in the `backend/` directory.

### Manual Setup
#### Backend
```bash
cd backend
python -m venv .venv
# Activate venv: .venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to start using the app.