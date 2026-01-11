class Categorizer:
    RULES = {
        "Food": [
            "RIMI", "MAXIMA", "LIDL", "MOGO", "TOP", "ELVI", "LATS", "SKY", "STOCKMANN", "PIGU", "220.LV", "BARBORA", "MR."
        ],
        "Dining": [
            "HESBURGER", "MCDONALDS", "KFC", "BURGER", "PIZZA", "PICA", "CAFE", "COFFEE", "RESTORANS", 
            "BISTRO", "WOLT", "BOLT FOOD", "LIDO", "GRILL", "SUSHI", "KEBAB"
        ],
        "Transport": [
            "CIRCLE K", "NESTE", "VIADA", "VIRSI", "KOOL", "SHELL", "GAS", "FUEL", 
            "BOLT", "UBER", "TAXI", "YANDEX", "PARKING", "EJUR", "RIGAS SATIKSME", "PASAZIERO VILCIENS", "LUX EXPRESS",
            "WASH AND DRIVE", "AUTODUALS"
        ],
        "Shopping": [
            "DEPO", "KSENUKAI", "IKEA", "JYSK", "KURSHI", "ZARA", "H&M", "PEPCO", "SINSAY", "RESERVED", "SPORTLAND", 
            "AMAZON", "EBAY", "ALIEXPRESS", "TEMU", "ABOUT YOU", "ZALANDO", "VEIKALS"
        ],
        "Utilities": [
            "ELEKTRUM", "TET", "TELE2", "BITE", "LMT", "LATTENS", "RIGAS SILTUMS", "RIGAS UDENS", "APS. MET", "NINE", 
            "BALTCOM", "LATVIJAS MOBILAIS TELEFONS"
        ],
        "Entertainment": [
            "NETFLIX", "SPOTIFY", "YOUTUBE", "STEAM", "PLAYSTATION", "XBOX", "APOLLO", "CINAMON", "BILESUS", "THEATRE"
        ],
        "Health": [
            "APTIEK", "PHARMACY", "POLIKLINIKA", "ARS", "VESELIBAS", "LIEPA", "MENESS"
        ],
        "Banking": [
            "KOMISIJA", "COMMISSION", "FEE", "INTRESES", "INTEREST", "CITADELE", "SWEDBANK", "SEB", "LUMINOR", "REVOLUT",
            "KARTES MĒNEŠA MAKSA", "ĀRVALSTU MAKSĀJUMU", "KPMG BALTICS"
        ],
        "Savings": [
            "KRAJKONTS", "SAVINGS", "DEPOSIT", "KRĀJRĪKĀ", "KRĀJRĪKS", "TRANSFER BETWEEN OWN ACCOUNTS"
        ]
    }

    def categorize(self, description: str) -> str:
        description_upper = description.upper()
        
        for category, keywords in self.RULES.items():
            for keyword in keywords:
                if keyword in description_upper:
                    return category
        
        return "Uncategorized"
