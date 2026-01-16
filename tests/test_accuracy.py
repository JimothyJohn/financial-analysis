from financial_analysis.__main__ import main
from financial_analysis.utils import get_income
from financial_analysis.filing_parser import FilingParser
from financial_analysis.config import SEC_API_KEY
import os
import logging


logging.basicConfig(
    level=logging.INFO, handlers=[logging.FileHandler(".logs/test_accuracy.log")]
)
logger = logging.getLogger(__name__)


class TestAccuracy:
    def test_ait_finances(self):
        filing_parser = FilingParser("ait", 2024, SEC_API_KEY)
        finances = get_income(filing_parser.filing, filing_parser.year)

        assert finances.Revenue["net"] == 4563424000
        assert finances.Costs["net"] == -3180265000
        assert finances.Operations["net"] == -884630000
        assert finances.Debt["net"] == -18214000
        assert finances.Taxes["net"] == -107979000
        assert finances.Investments["net"] == 17602000
        assert finances.CurrencyExchange["net"] == -1655000

    """
    assert finances.Expenses is not None
    assert finances.Benefits is not None
    assert finances.Reclassification is not None
    assert finances.IncomeLossTax is not None
    """

    def test_gpc_finances(self):
        filing_parser = FilingParser("gpc", 2025, SEC_API_KEY)
        finances = get_income(filing_parser.filing, filing_parser.year)

        assert finances.Revenue["net"] == 23486569000
        assert finances.Costs["net"] == -14962954000
        assert finances.Operations["net"] == -6642900000
        assert finances.Debt["net"] == -96827000
        assert finances.Taxes["net"] == -271892000
        assert finances.Investments["net"] == 0
