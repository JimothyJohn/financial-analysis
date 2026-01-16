import os
import argparse
import logging
from financial_analysis.filing_parser import FilingParser
from financial_analysis.config import SEC_API_KEY
from financial_analysis.models import Income

# Writes log files toa folde rcalled .logs/
logging.basicConfig(
    level=logging.INFO, handlers=[logging.FileHandler(".logs/financial_analysis.log")]
)

logger = logging.getLogger(__name__)

parser: argparse.ArgumentParser = argparse.ArgumentParser()

parser.add_argument(
    "-c",
    "--company",
    type=str,
    help="Stock symbol of company to analyze",
    default="aapl",
)
parser.add_argument("-y", "--year", type=int, help="Year to query", default=2025)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output directory for filings",
    default="outputs/2025",
)


def main(company: str = "aapl", year: int = 2025, output: str = "outputs/2025") -> None:
    if company == "aapl":
        logger.info("\tRunning for Apple Computer Company Inc\n")

    filing_parser = FilingParser(company, year, SEC_API_KEY)

    # Print all values except those that have a net of 0 and format the value like a currency
    print("\n\t2025\n")
    for key, value in filing_parser.income.model_dump().items():
        if isinstance(value, int):
            if value != 0:
                print(f"\t{key}\n\t${value:,}")
            continue

        if value.get("net") != 0:
            print(f"\t{key}\n\t${value['net']:,}\n")

    # print(filing_parser.income.model_dump_json(indent=4))

def get_keywords(financeModel):
    for field in financeModel.model_fields:
        print(field)

    # Put the keywords from the Income fields into a list
    return [
        keyword
        for val in income.model_dump().values()
        if isinstance(val, dict) and "keywords" in val
        for keyword in val["keywords"]
    ]

def get_values(filingCategory: dict, index: int) -> any:
    keywords = get_keywords()

    for key in filingCategory.keys():
        for field in keywords:
            if field.name == key:
                return filingCategory[key][index]

    return None

    
if __name__ == "__main__":
    income: Income = Income()
    get_keywords(income)
    args: argparse.Namespace = parser.parse_args()
    main(args.company.lower(), args.year, args.output)
