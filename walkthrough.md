# Walkthrough: Personal Finance Filter Updates

## What was done
1.  **Date Filtering**:
    - Added "From" and "To" date pickers to the dashboard.
    - Updated backend algorithms to filter transactions by precise dates.
    - Included "Year" view for quick annual analysis.

2.  **Advanced Filtering**:
    - Added **Category Dropdown**: Select a specific category (e.g., "Food", "Savings") to see analytics just for that type.
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

## How to use
1.  **Select Period**: Click "Month" or "Year".
2.  **Date Range**: (Optional) Pick specific start/end dates.
3.  **Filter**: Choose a Category from the dropdown or type in the search box.
4.  **View Results**: Charts and totals automatically update.
5.  **Export**: Click "Export PDF" to get a report matching your current view.
