from sqlalchemy.orm import Session
from models import SessionLocal, Transaction
from collections import Counter

def analyze_uncategorized():
    db = SessionLocal()
    try:
        txns = db.query(Transaction).filter(Transaction.category == "Uncategorized").all()
        descriptions = [t.description for t in txns]
        
        print(f"Total Uncategorized: {len(descriptions)}")
        print("--- Top 20 Uncategorized Descriptions ---")
        
        # Count frequency to prioritize common merchants
        counts = Counter(descriptions)
        for desc, count in counts.most_common(20):
            print(f"{count}x : {desc}")
            
    finally:
        db.close()

if __name__ == "__main__":
    analyze_uncategorized()
