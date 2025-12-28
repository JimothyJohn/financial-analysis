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

    print(f"\t{args.company.upper()} made ${analyst.Filing.StatementsOfComprehensiveIncome.ComprehensiveIncome:,.0f} in {args.year}")


if __name__ == "__main__":
    main()
