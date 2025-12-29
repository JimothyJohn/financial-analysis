import os
import argparse
import logging
from analyst import Analyst
from dotenv import load_dotenv

load_dotenv()

# Load API_KEY
SEC_API_KEY: str = str(f"{os.environ.get("SEC_API_KEY")}")

# Writes log files toa folde rcalled .logs/
logging.basicConfig(
    level=logging.INFO, handlers=[logging.FileHandler(".logs/financial_analysis.log")]
)

logger = logging.getLogger(__name__)

parser: argparse.ArgumentParser = argparse.ArgumentParser()

parser.add_argument("-c", "--company", type=str, help="Stock symbol of company to analyze", default="aapl")
parser.add_argument("-y", "--year", type=int, help="Year to query", default=2025)
parser.add_argument("-o", "--output", type=str, help="Output directory for filings", default="outputs/2025")
args: argparse.Namespace = parser.parse_args()

logger.info("")

def main() -> None:
    if os.path.exists(f"{args.output}/{args.company} 10-k.json"):
        logger.info(
            "\tINEFFICIENT: JSON already extracted, downloading new one though...\n"
        )
        # exit()

    if args.company == "aapl":
        logger.info("\tRunning for Apple Computer Company Inc\n")

    analyst = Analyst(args.company, args.year, SEC_API_KEY)

    soi = analyst.Filing.StatementsOfIncome
    debt = 0
    if soi.Debt:
        debt = soi.Debt

    print(f"\n\tIn {args.year}, {args.company.upper()} made ${analyst.Filing.StatementsOfComprehensiveIncome.ComprehensiveIncome:,.0f}:\n")
    print(f"\t${soi.Revenue:,.0f}\t\tRevenue")
    print(f"\t-${soi.Costs:,.0f}\t\tCOGS")
    print(f"\t${soi.Revenue - soi.Costs:,.0f}\t\tGross Profit")
    print(f"\t-${soi.Operations:,.0f}\t\tOperations")
    print(f"\t${soi.Revenue - soi.Costs - soi.Operations:,.0f}\t\tEBIDTA")
    print(f"\t-${soi.Expenses:,.0f}\t\tOther Expenses")
    print(f"\t-${soi.Taxes:,.0f}\t\tTaxes")
    print(f"\t-${debt:,.0f}\t\tDebt")
    print(f"\t${soi.Revenue - soi.Costs - soi.Operations - soi.Expenses - soi.Taxes - debt:,.0f}\t\tNet Income\n")


    print(f"\t${analyst.Filing.BalanceSheets.Cash:,.0f}\t\tCash")
    print(f"\t${analyst.Filing.BalanceSheets.Assets:,.0f}\t\tAssets")
    print(f"\t${analyst.Filing.BalanceSheets.Equity:,.0f}\t\tEquity")

if __name__ == "__main__":
    main()
