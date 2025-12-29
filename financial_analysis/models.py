from pydantic import BaseModel
from typing import Optional

class CoverPage(BaseModel):
    DocumentType: str
    DocumentPeriodEndDate: str

class StatementsOfIncome(BaseModel):
    Revenue: int
    Costs: int
    Operations: int
    Debt: Optional[int]
    Expenses: int
    Taxes: int
    # InterestIncome: Optional[int] = None

class StatementsOfComprehensiveIncome(BaseModel):
    ComprehensiveIncome: int

class StatementsOfCashFlows(BaseModel):
    Income: int

class BalanceSheets(BaseModel):
    Cash: int
    Assets: int
    Liabilities: int
    Equity: int

class Filing(BaseModel):
    CoverPage: Optional[CoverPage]
    StatementsOfIncome: StatementsOfIncome
    StatementsOfComprehensiveIncome: StatementsOfComprehensiveIncome
    StatementsOfCashFlows: StatementsOfCashFlows
    BalanceSheets: BalanceSheets

class Keys(BaseModel):
    revenue: str
    costs: str
    operations: str
    debt: Optional[str]
    taxes: str
    expenses: str
    # interest_income: str
    comprehensive_income: str
    cash_flow: str
    cash: str
    assets: str
    liabilities: str
    equity: str
