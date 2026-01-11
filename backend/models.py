from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

SQLAPLCHEMY_DATABASE_URL = "sqlite:///./finance.db"

engine = create_engine(
    SQLAPLCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(Date)
    
    transactions = relationship("Transaction", back_populates="statement", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    statement_id = Column(Integer, ForeignKey("statements.id"))
    date = Column(Date, index=True)
    description = Column(String)
    amount = Column(Float) # Positive for income, negative for expense? Or separate column? 
                           # Convention: Amount is signed. + for income, - for expense is common.
                           # Additional type column could be useful: 'income' | 'expense'
    category = Column(String, nullable=True) # For future auto-categorization
    
    statement = relationship("Statement", back_populates="transactions")

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Tables created.")
