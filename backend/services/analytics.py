import pandas as pd
from sqlalchemy.orm import Session
from models import Transaction

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_transactions_dataframe(self, statement_id=None, start_date=None, end_date=None, category=None, search=None):
        query = self.db.query(Transaction)
        if statement_id:
            query = query.filter(Transaction.statement_id == statement_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
            
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        if category and category != "All":
            query = query.filter(Transaction.category == category)
            
        if search:
            # Case-insensitive substring match
            search_pattern = f"%{search}%"
            query = query.filter(Transaction.description.ilike(search_pattern))
        
        transactions = query.all()
        if not transactions:
            return pd.DataFrame()

        data = [
            {
                "date": t.date,
                "description": t.description,
                "amount": t.amount,
                "category": t.category
            }
            for t in transactions
        ]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_summary_by_period(self, period='M', start_date=None, end_date=None, category=None, search=None):
        """
        Groups data by period.
        period: 'D' (Day), 'W' (Week), 'M' (Month)
        """
        df = self.get_transactions_dataframe(start_date=start_date, end_date=end_date, category=category, search=search)
        if df.empty:
            return []

        # Additional safety: ensure we resort index if needed, though pandas Usually handles it.
        # Ensure df is sorted by date before resampling if needed, though resample on 'date' column generally works.
        
        # Income vs Expenses
        income = df[df['amount'] > 0].resample(period, on='date')['amount'].sum().fillna(0)
        expenses = df[df['amount'] < 0].resample(period, on='date')['amount'].sum().fillna(0) # Keep negative
        
        # Combine
        combined = pd.DataFrame({'income': income, 'expenses': expenses})
        combined['net'] = combined['income'] + combined['expenses']
        
        # Sort by date
        combined.sort_index(inplace=True)
        
        # Format for frontend
        results = []
        for date, row in combined.iterrows():
            results.append({
                "date": date.strftime('%Y-%m-%d'),
                "income": float(row['income']),
                "expenses": float(row['expenses']),
                "net": float(row['net'])
            })
            
        return results

    def get_total_balance(self):
        df = self.get_transactions_dataframe()
        if df.empty:
            return 0.0
        return float(df['amount'].sum())

    def get_category_breakdown(self, period='M', start_date=None, end_date=None, category=None, search=None):
        df = self.get_transactions_dataframe(start_date=start_date, end_date=end_date, category=category, search=search)
        if df.empty:
            return []
        
        # Filter expenses only (negative amounts)
        expenses_df = df[df['amount'] < 0].copy()
        if expenses_df.empty:
            return []
            
        # Group by category
        # Using abs() effectively to show positive values for pie chart
        expenses_df['abs_amount'] = expenses_df['amount'].abs()
        grouped = expenses_df.groupby('category')['abs_amount'].sum()
        
        results = []
        for category, amount in grouped.items():
            results.append({
                "name": category,
                "value": float(amount)
            })
            
        # Sort by value desc
        results.sort(key=lambda x: x['value'], reverse=True)
        return results
