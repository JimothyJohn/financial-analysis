import logging
import json
import gzip
from sec_api import QueryApi
from sec_api import RenderApi
from sec_api import XbrlApi
from financial_analysis.models import (
    CoverPage,
    Income,
)
from typing import Optional
from financial_analysis.config import WHITELIST
from financial_analysis.utils import get_value, get_income
import urllib.request
import os

logging.basicConfig(level=logging.INFO, handlers=[])

logger = logging.getLogger(__name__)


class FilingParser:
    def __init__(self, company: str, year: int, api_key: str) -> None:
        assert company in WHITELIST, "Company not supported"
        self.company = company
        self.year = year
        self.renderApi = RenderApi(api_key=api_key)
        self.xbrlApi = XbrlApi(api_key)
        self.queryApi = QueryApi(api_key=api_key)
        self._get_filing_as_json(company)
        self._factory()

    def _get_filing_as_json(self, company: str, save: bool = True) -> None:
        if os.path.exists(f"outputs/{self.year}/{self.company}_10-K.json"):
            with open(f"outputs/{self.year}/{self.company}_10-K.json", "r") as f:
                self.filing = json.load(f)
            return

        # TODO Try some good old fashioned SQL injection here
        query = {
            "query": f'ticker:{company} AND formType:"10-K"',
            "from": "0",
            "size": "10",
            "sort": [{"filedAt": {"order": "desc"}}],
        }

        filings = self.queryApi.get_filings(query)
        if len(filings["filings"]) == 0:
            raise Exception("No filings found")
        filingUrl: str = filings["filings"][0]["linkToFilingDetails"]

        # 10-K HTM File URL example
        self.filing = self.xbrlApi.xbrl_to_json(htm_url=filingUrl)
        if save:
            try:
                response = urllib.request.urlopen(
                    urllib.request.Request(
                        filingUrl,
                        headers={
                            "User-Agent": "Nick<nick@nick.com>",
                            "Accept-Encoding": "gzip, deflate",
                            "Host": "www.sec.gov",
                        },
                    )
                )
                data = response.read()

                # Check for gzip compression
                if response.info().get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)

                with open(f"outputs/2025/{self.company}_10-K.htm", "wb") as f:
                    f.write(data)

            except Exception as e:
                print(f"An error occurred: {e}")

            with open(f"outputs/2025/{self.company}_10-k.json", "w") as f:
                f.write(json.dumps(self.filing, indent=4))

    def _factory(self) -> None:
        cp: Optional[CoverPage] = None
        if self.filing.get("CoverPage") is not None:
            cp = CoverPage(
                DocumentType=get_value(self.filing["CoverPage"]["DocumentType"]),
                DocumentPeriodEndDate=get_value(
                    self.filing["CoverPage"]["DocumentPeriodEndDate"]
                ),
            )
            self.year = int(cp.DocumentPeriodEndDate[:4])

        assert self.year is not None, "Period end date not found"

        self.income: Income = get_income(self.filing, self.year)
