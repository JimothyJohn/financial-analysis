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
    Equity: Optional[int]


class Filing(BaseModel):
    CoverPage: Optional[CoverPage]
    StatementsOfIncome: StatementsOfIncome
    StatementsOfComprehensiveIncome: StatementsOfComprehensiveIncome
    StatementsOfCashFlows: StatementsOfCashFlows
    BalanceSheets: BalanceSheets


class Keys(BaseModel):
    # TODO: Maybe convert to str, more conveenient when everythign is a list, though
    revenue: list[str]
    costs: list[str]
    operations: list[str]
    debt: Optional[list[str]]
    taxes: list[str]
    expenses: list[str]
    # interest_income: str
    # TODO: Calculate this automatically
    comprehensive_income: list[str]
    cash_flow: list[str]
    cash: list[str]
    assets: list[str]
    liabilities: list[str]
    equity: list[str]


class Finances(BaseModel):
    Revenue: int
    Costs: int
    GrossProfit: int
    Operations: int
    EBITDA: int
    Expenses: int
    Investments: int
    Debt: int
    Taxes: int
    CurrencyExchange: int
    Benefits: int
    Reclassification: int
    IncomeLossTax: int
    NetIncome: int
