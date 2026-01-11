from services.pdf_parser import PDFParser
import os

def debug():
    parser = PDFParser()
    file_path = os.path.join("uploads", "statement2025.pdf")
    
    print(f"DEBUGGING FILE: {file_path}")
    if not os.path.exists(file_path):
        print("File not found!")
        return

    try:
        transactions = parser.parse_statement(file_path)
        print(f"FOUND {len(transactions)} TRANSACTIONS")
        for t in transactions:
            print(t)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug()
