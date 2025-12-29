import logging
import json
import gzip
from sec_api import QueryApi
from sec_api import RenderApi
from sec_api import XbrlApi
from models import Filing, CoverPage, StatementsOfIncome, StatementsOfComprehensiveIncome, StatementsOfCashFlows, BalanceSheets
from config import WHITELIST
from utils import get_value, get_keys
import urllib.request

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
        self.keys = get_keys(self.filing)
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
            try:
                response = urllib.request.urlopen(urllib.request.Request(
                    filingUrl,
                    headers={
                        "User-Agent": "Nick<nick@nick.com>",
                        "Accept-Encoding": "gzip, deflate",
                        "Host": "www.sec.gov"
                    },))
                data = response.read()
                
                # Check for gzip compression
                if response.info().get('Content-Encoding') == 'gzip':
                    data = gzip.decompress(data)
                
                with open(f"outputs/2025/{self.company}_10-K.htm", "wb") as f:
                    f.write(data)

            except Exception as e:
                print(f"An error occurred: {e}")

            with open(f"outputs/2025/{self.company}_10-k.json", "w") as f:
                f.write(json.dumps(self.filing, indent=4))

    def _gaap_int(self, key: str, category: str) -> int:
        return int(get_value(self.filing[category][key][self.index]))

    def _factory(self) -> None:
        keys = get_keys(self.filing)

        cp: CoverPage = None 
        if self.filing.get("CoverPage") is not None:
            cp = CoverPage(
                DocumentType=get_value(self.filing["CoverPage"]["DocumentType"]),
                DocumentPeriodEndDate=get_value(self.filing["CoverPage"]["DocumentPeriodEndDate"]),
        )

        self.Filing: Filing = Filing(
            CoverPage=cp,
            StatementsOfIncome=StatementsOfIncome(
                Revenue=self._gaap_int(keys.revenue, "StatementsOfIncome"),
                Costs=self._gaap_int(keys.costs, "StatementsOfIncome"),
                Operations=self._gaap_int(keys.operations, "StatementsOfIncome"),
                Debt=self._gaap_int(keys.debt, "StatementsOfIncome") if keys.debt else None,
                Taxes=self._gaap_int(keys.taxes, "StatementsOfIncome"),
                Expenses=self._gaap_int(keys.expenses, "StatementsOfIncome"),
            ),
            StatementsOfComprehensiveIncome=StatementsOfComprehensiveIncome(
                ComprehensiveIncome=self._gaap_int(keys.comprehensive_income, "StatementsOfComprehensiveIncome"),),
            StatementsOfCashFlows=StatementsOfCashFlows(
                Income=self._gaap_int(keys.cash_flow, "StatementsOfCashFlows"),),
            BalanceSheets=BalanceSheets(
                Cash=self._gaap_int(keys.cash, "BalanceSheets"),
                Assets=self._gaap_int(keys.assets, "BalanceSheets"),
                Liabilities=self._gaap_int(keys.liabilities, "BalanceSheets"),
                Equity=self._gaap_int(keys.equity, "BalanceSheets")),
        )