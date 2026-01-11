import pdfplumber
import re
from datetime import datetime

class PDFParser:
    def __init__(self):
        pass

    def parse_statement(self, file_path):
        """
        Parses a PDF bank statement and returns a list of transactions.
        
        Returns:
            list[dict]: A list of transaction dictionaries with keys:
                        'date', 'description', 'amount'.
        """
        transactions = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                print(f"--- PROCESSING PAGE {page.page_number} ---", flush=True)
                text = page.extract_text()
                if not text:
                    print("NO TEXT FOUND ON PAGE", flush=True)
                    continue
                
                print(f"--- TEXT CONTENT ---", flush=True)
                print(text, flush=True)
                print("--- END DEBUG PAGE ---", flush=True)

                # Basic heuristic parsing (Placeholder)
                # This assumes a line looks like: "DATE DESCRIPTION AMOUNT"
                # We need actual samples to make this robust.
                lines = text.split('\n')
                for line in lines:
                    txn = self._parse_line(line)
                    if txn:
                        transactions.append(txn)
                        
        return transactions

    def _parse_line(self, line):
        # Swedbank format ID: "83 21.01.2025 ..."
        # Regex to find the start: Number + Date
        try:
            # Match start of line: sequence number + date (DD.MM.YYYY)
            match_start = re.match(r'^(\d+)\s+(\d{2}\.\d{2}\.\d{4})', line)
            if not match_start:
                return None
            
            date_str = match_start.group(2)
            
            # Find all numbers that look like amounts (including spaces like "-3 000.00")
            # Pattern: optional minus, digits/spaces, dot/comma, 2 digits, end of word/line
            # This is tricky because "3.90" is an amount, "5573..." is card number.
            # Card numbers don't usually have decimals.
            
            # Strategy: Split line by Date. Take the right part.
            after_date = line[match_start.end():]
            
            # Find candidate amounts (numbers with decimal part)
            # Regex: negative? space? digits (space digits)* [.,] digits{2}
            amount_matches = list(re.finditer(r'(-?[\d\s]+[.,]\d{2})(?!\d)', after_date))
            
            if not amount_matches:
                return None
                
            # Usually the last number is Balance, 2nd to last is Transaction Amount.
            # However, sometimes there might be other numbers.
            # Let's take the last two.
            if len(amount_matches) >= 2:
                amount_str = amount_matches[-2].group(1)
            else:
                amount_str = amount_matches[-1].group(1)
                
            # Clean amount string (remove spaces, replace comma)
            clean_amount = amount_str.replace(' ', '').replace(',', '.')
            amount = float(clean_amount)
            
            # Description is everything between Date and Amount
            # Start of description = 0 (relative to after_date)
            # End of description = start of amount match
            desc_end = amount_matches[-2].start() if len(amount_matches) >= 2 else amount_matches[-1].start()
            description = after_date[:desc_end].strip()
            
            # Parse date
            date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()

            return {
                'date': date_obj,
                'description': description,
                'amount': amount
            }
        except Exception as e:
            print(f"Error parsing line: {line} -> {e}", flush=True)
            return None
