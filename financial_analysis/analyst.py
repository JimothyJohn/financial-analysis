import logging
import json
from sec_api import QueryApi
from sec_api import RenderApi
from sec_api import XbrlApi
from models import Filing, CoverPage, StatementsOfIncome, StatementsOfComprehensiveIncome, Keys
from config import WHITELIST
from utils import get_value

logging.basicConfig(level=logging.INFO, handlers=[])

logger = logging.getLogger(__name__)


class Analyst:
    def __init__(self, company: str, year: int, api_key: str) -> None:
        assert company in WHITELIST, "Company not supported"
        self.company = company
        self.index = 2025 - year
        self.renderApi = RenderApi(api_key=api_key)
        self.xbrlApi = XbrlApi(api_key)
        self.queryApi = QueryApi(api_key=api_key)
        self._get_filing_as_json(company)
        self._get_keys()
        self._factory()

    def _get_filing_as_json(self, company: str, save: bool = True) -> None:
        # TODO Try some good old fashioned SQL injection here
        query = {
            "query": f'ticker:{company} AND formType:"10-K"',
            "from": "0",
            "size": "10",
            "sort": [{"filedAt": {"order": "desc"}}],
        }

        filings = self.queryApi.get_filings(query)
        filingUrl: str = filings["filings"][self.index]["linkToFilingDetails"]

        # 10-K HTM File URL example
        self.filing = self.xbrlApi.xbrl_to_json(htm_url=filingUrl)
        if save:
            with open(f"outputs/2025/{self.company} 10-k.json", "w") as f:
                f.write(json.dumps(self.filing, indent=4))

    def _get_keys(self) -> None:
        # Find keys for income statement items
        for key in self.filing["StatementsOfIncome"].keys():
            if "NetIncome" in key:
                net_income_key = key
            elif "CostOf" in key:
                cogs_key = key
            elif "Profit" in key:
                gross_profit_key = key
            
        comprehensive_key = next((k for k in self.filing["StatementsOfComprehensiveIncome"].keys() if "ComprehensiveIncomeNetOfTax" in k), "")

        assert cogs_key, "COGS not found" 
        assert gross_profit_key, "Gross Profit not found" 
        assert net_income_key, "Net Income not found" 
        assert comprehensive_key, "Comprehensive Income not found" 

        self.keys = Keys(
            net_income=net_income_key,
            cost_of_goods_sold=cogs_key,
            gross_profit=gross_profit_key,
            comprehensive_income=comprehensive_key
        )

    def _factory(self) -> None:
        self.Filing: Filing = Filing(
            CoverPage=CoverPage(
                DocumentType=get_value(self.filing["CoverPage"]["DocumentType"]),
                DocumentPeriodEndDate=get_value(self.filing["CoverPage"]["DocumentPeriodEndDate"]),
            ),
            StatementsOfIncome=StatementsOfIncome(
                GrossProfit=int(get_value(self.filing["StatementsOfIncome"][self.keys.gross_profit][self.index])),
                CostOfGoodsSold=int(get_value(self.filing["StatementsOfIncome"][self.keys.cost_of_goods_sold][self.index])),
                NetIncome=int(get_value(self.filing["StatementsOfIncome"][self.keys.net_income][self.index]))),
            StatementsOfComprehensiveIncome=StatementsOfComprehensiveIncome(
                ComprehensiveIncome=int(get_value(self.filing["StatementsOfComprehensiveIncome"][self.keys.comprehensive_income][self.index])))
        )

