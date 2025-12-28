import logging
import json
from sec_api import QueryApi
from sec_api import RenderApi
from sec_api import XbrlApi

logging.basicConfig(level=logging.INFO, handlers=[])

logger = logging.getLogger(__name__)


class Analyst:
    def __init__(self, company: str, year: int, api_key: str) -> None:
        assert company in [
            "aapl",
            "ait",
            "nvda",
            "tsla",
            "amzn",
            "amd",
            "f",
            "intc",
            "msft",
            "gpc",
        ], "Company not supported"
        self.company = company
        self.index = 2025 - year
        self.renderApi = RenderApi(api_key=api_key)
        self.xbrlApi = XbrlApi(api_key)
        self.queryApi = QueryApi(api_key=api_key)
        self.filing: dict = None

    def _get_filing_as_json(self, company: str):
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
        with open(f"outputs/2025/{self.company} 10-k.json", "w") as f:
            f.write(json.dumps(self.filing, indent=4))

    def extract_gross_profit(self, soi: dict) -> int:
        for key in soi.keys():
            if "GrossProfit" in key:
                self.gross_profit = int(soi[key][self.index]["value"])
                print(
                    f"\t{self.company.upper()} {2025-self.index} Gross Profit: ${self.gross_profit:,.0f}"
                )
                return self.gross_profit
        raise ValueError("GrossProfit not found")

    def extract_cogs(self, soi: dict) -> int:
        for key in soi.keys():
            if "CostOfGoods" in key:
                self.cogs = int(soi[key][self.index]["value"])
                print(
                    f"\t{self.company.upper()} {2025-self.index} Cost of Goods Sold: ${self.cogs:,.0f}"
                )
                return self.cogs

        raise ValueError("COGS not found")

    def _extract_net_income(self, soci: dict) -> int:
        for key in soci.keys():
            if "ComprehensiveIncomeNetOfTax" in key:
                self.net_income = int(
                    self.filing["StatementsOfComprehensiveIncome"][key][0]["value"]
                )
                return self.net_income
        raise ValueError("ComprehensiveIncomeNetOfTax not found")

    def _extract_comprehensive_net_income(self, soci: dict) -> int:
        for key in soci.keys():
            if "Comprehensive" in key:
                self.net_income = int(self.filing[key])
                return self.net_income
        raise ValueError("ComprehensiveIncomeNetOfTax not found")

    def get_comprehensive_income_net_of_tax(self) -> int:

        self._get_filing_as_json(self.company)
        self.net_income = self._extract_net_income(
            self.filing["StatementsOfComprehensiveIncome"]
        )

        return self.net_income
