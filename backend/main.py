from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from datetime import date

from models import SessionLocal, init_db, Statement, Transaction
from services.pdf_parser import PDFParser
from services.analytics import AnalyticsService
from services.report_generator import ReportGenerator
from services.categorizer import Categorizer

app = FastAPI(title="Personal Finance Analyzer")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize DB on startup
# In newer FastAPI we might use lifespan, but this is simple enough for now
init_db()

# Services
pdf_parser = PDFParser()
report_gen = ReportGenerator()
categorizer = Categorizer()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "API Running"}

@app.post("/categorize")
def categorize_all(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    count = 0
    for txn in transactions:
        old_cat = txn.category
        new_cat = categorizer.categorize(txn.description)
        if old_cat != new_cat:
            txn.category = new_cat
            count += 1
    
    db.commit()
    return {"message": f"Updated {count} transactions"}

@app.post("/upload")
async def upload_statements(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []
    
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse PDF
        try:
            transactions_data = pdf_parser.parse_statement(file_location)
            
            if not transactions_data:
                results.append({"filename": file.filename, "status": "error", "message": "No transactions found"})
                continue

            # Save to DB
            # Create Statement record
            db_statement = Statement(filename=file.filename, upload_date=date.today())
            db.add(db_statement)
            db.commit()
            db.refresh(db_statement)
            
            # Create Transactions
            for txn in transactions_data:
                # Auto-categorize immediately on upload
                cat = categorizer.categorize(txn['description'])
                
                db_txn = Transaction(
                    statement_id=db_statement.id,
                    date=txn['date'],
                    description=txn['description'],
                    amount=txn['amount'],
                    category=cat
                )
                db.add(db_txn)
            
            db.commit()
            results.append({"filename": file.filename, "status": "success", "count": len(transactions_data)})
            
        except Exception as e:
            results.append({"filename": file.filename, "status": "error", "message": str(e)})

    return {"message": "Processing complete", "details": results}

@app.get("/categories")
def get_unique_categories(db: Session = Depends(get_db)):
    # Get distinct categories from DB
    cats = db.query(Transaction.category).distinct().all()
    # cats is list of tuples [('Food',), ('Transport',)]
    return [c[0] for c in cats if c[0]]

@app.get("/analysis")
def get_analysis(
    period: str = 'M', 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    analytics = AnalyticsService(db)
    # period mapping: frontend might send 'day', 'week', 'month'
    # pandas resample uses 'D', 'W', 'M'
    p_map = {'day': 'D', 'week': 'W', 'month': 'M', 'year': 'A'}
    p = p_map.get(period.lower(), 'M')
    
    summary = analytics.get_summary_by_period(p, start_date=start_date, end_date=end_date, category=category, search=search)
    breakdown = analytics.get_category_breakdown(p, start_date=start_date, end_date=end_date, category=category, search=search)
    
    return {
        "summary": summary,
        "breakdown": breakdown
    }

@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    analytics = AnalyticsService(db)
    df = analytics.get_transactions_dataframe()
    if df.empty:
        return []
    # Convert date to string for JSON
    res = df.to_dict(orient='records')
    for r in res:
        r['date'] = r['date'].strftime('%Y-%m-%d')
    return res

@app.get("/report")
def generate_report(
    period: str = 'M', 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    analytics = AnalyticsService(db)
    p_map = {'day': 'D', 'week': 'W', 'month': 'M', 'year': 'A'}
    p = p_map.get(period.lower(), 'M')
    
    data = analytics.get_summary_by_period(p, start_date=start_date, end_date=end_date, category=category, search=search)
    
    report_filename = f"report_{period}.pdf"
    report_gen.generate_report(data, filename=report_filename)
    
    return FileResponse(report_filename, media_type='application/pdf', filename=report_filename)
