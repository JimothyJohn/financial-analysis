import json
import logging
import os

from financial_analysis import edgar
from financial_analysis.config import WHITELIST
from financial_analysis.models import (
    CoverPage,
    Income,
)
from financial_analysis.utils import get_income, get_value

logging.basicConfig(level=logging.INFO, handlers=[])

logger = logging.getLogger(__name__)


class FilingParser:
    def __init__(self, company: str, year: int) -> None:
        assert company in WHITELIST, "Company not supported"
        self.company = company
        self.year = year
        self._get_filing_as_json(company)
        self._factory()

    def _cache_path(self) -> str:
        return f"outputs/{self.year}/{self.company}_10-K.json"

    def _get_filing_as_json(self, company: str, save: bool = True) -> None:
        if os.path.exists(self._cache_path()):
            with open(self._cache_path(), "r") as f:
                self.filing = json.load(f)
            return

        self.filing, filing_url = edgar.get_filing_json(company, self.year)

        if save:
            os.makedirs(f"outputs/{self.year}", exist_ok=True)
            with open(self._cache_path(), "w") as f:
                f.write(json.dumps(self.filing, indent=4))

            try:
                data = edgar._get(filing_url)
                with open(f"outputs/{self.year}/{self.company}_10-K.htm", "wb") as f:
                    f.write(data)
            except OSError as e:
                logger.error("Could not save filing document: %s", e)

    def _factory(self) -> None:
        cp: CoverPage | None = None
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
