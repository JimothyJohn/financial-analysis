from pydantic import BaseModel

class CoverPage(BaseModel):
    DocumentType: str
    DocumentPeriodEndDate: str

class StatementsOfIncome(BaseModel):
    GrossProfit: int
    CostOfGoodsSold: int
    NetIncome: int

class StatementsOfComprehensiveIncome(BaseModel):
    ComprehensiveIncome: int

class Filing(BaseModel):
    CoverPage: CoverPage
    StatementsOfIncome: StatementsOfIncome
    StatementsOfComprehensiveIncome: StatementsOfComprehensiveIncome

class Keys(BaseModel):
    net_income: str
    cost_of_goods_sold: str
    gross_profit: str
    comprehensive_income: str
