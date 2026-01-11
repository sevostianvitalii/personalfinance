# Walkthrough: Personal Finance Filter Updates

## What was done
1.  **Date Filtering**:
    - Added "From" and "To" date pickers to the dashboard.
    - Updated backend algorithms to filter transactions by precise dates.
    - Included "Year" view for quick annual analysis.

2.  **Advanced Filtering**:
    - Added **Category Dropdown**: Select a specific category (e.g., "Savings") to see analytics just for that type.
    - Added **Search Bar**: Type any text (e.g., "Rimi") to find transactions by description or recipient.
    - **Combined Logic**: All filters work together (e.g., "Savings" in "2024" matching "Bank").

3.  **UI Improvements**:
    - Fixed chart resizing issues.
    - Added detailed "Expenses by Category" list with exact amounts next to the pie chart.
    - Improved responsiveness of the dashboard layout.

4.  **GitHub Setup**:
    - Initialized a secure git repository.
    - Created `.gitignore` to exclude sensitive data (DB, uploads).
    - Pushed code to [GitHub](https://github.com/sevostianvitalii/personalfinance).

5.  **Dockerization**:
    - Created `Dockerfile` for Backend and Frontend.
    - Created `docker-compose.yml` for easy one-command start.

## How to use
**(New) Running with Docker**:
1.  Ensure you have Docker Desktop installed.
2.  Run `docker-compose up --build`.
3.  Open http://localhost:5173.

**Filters usage**:
1.  **Select Period**: Click "Month" or "Year".
2.  **Filter**: Choose a Category from the dropdown or type in the search box.
3.  **View Results**: Charts and totals automatically update.
4.  **Export**: Click "Export PDF" to get a report matching your current view.
