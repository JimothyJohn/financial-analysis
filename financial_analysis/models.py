from pydantic import BaseModel
from typing import Optional


class CoverPage(BaseModel):
    DocumentType: str
    DocumentPeriodEndDate: str


class BalanceSheet(BaseModel):
    Cash: dict = {"net": 0}
    Assets: dict = {"net": 0}
    Liabilities: dict = {"net": 0}
    Equity: Optional[dict] = {"net": 0}


class Income(BaseModel):
    Revenue: dict = {"net": 0, "keywords": ["Revenue"]}
    Costs: dict = {"net": 0, "keywords": ["CostOf"]}
    GrossProfit: dict = {"net": 0}
    Operations: dict = {"net": 0, "keywords": ["Administrative"]}
    EBITDA: dict = {"net": 0}
    Expenses: dict = {"net": 0, "keywords": ["Expense", "Depreciat", "Restructur"]}
    Investments: dict = {"net": 0, "keywords": ["Investment"]}
    Debt: dict = {"net": 0, "keywords": ["Interest", "Expense"]}
    Taxes: dict = {"net": 0, "keywords": ["Tax"]}
    CurrencyExchange: dict = {"net": 0, "keywords": ["Currency"]}
    Benefits: dict = {"net": 0, "keywords": ["etirement"]}
    Reclassification: dict = {"net": 0, "keywords": ["lassification"]}
    IncomeLossTax: dict = {"net": 0, "keywords": ["IncomeLossTax"]}
    NetIncome: dict = {"net": 0}
