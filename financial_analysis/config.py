import os

from dotenv import load_dotenv

load_dotenv()

SEC_API_KEY = str(f"{os.environ.get('SEC_API_KEY')}")

WHITELIST = [
    "aapl",
    "ait",
    "cron",
    "nvda",
    "amzn",
    "amd",
    "f",
    "intc",
    "msft",
    "pcg",
    "gpc",
    "ge",
    "jakk",
]
