from financial_analysis.models import Income
from financial_analysis.models import BalanceSheet
import logging

logger = logging.getLogger(__name__)


def get_value(data, key: str = "value") -> str:
    """
    Helper to safely extract values from dict, list, or string.
    Doesn't work for this scenario:

        "TradingSymbol": [
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:CommonStockNoParValueMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "exch:XNYS"
                    }
                ],
                "value": "PCG"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare6NonredeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PA"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare5.50NonredeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PB"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare5NonredeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PC"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare5RedeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PD"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare5SeriesARedeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PE"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare4.80RedeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PG"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare4.50RedeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PH"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:FirstPreferredStockCumulativeParValue25PerShare4.36SeriesARedeemableMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "pcg:NYSEAMERICANLLCMember"
                    }
                ],
                "value": "PCG-PI"
            },
            {
                "period": {
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                "segment": [
                    {
                        "dimension": "us-gaap:StatementClassOfStockAxis",
                        "value": "pcg:A6.000SeriesAMandatoryConvertiblePreferredStockMember"
                    },
                    {
                        "dimension": "dei:EntityListingsExchangeAxis",
                        "value": "exch:XNYS"
                    }
                ],
                "value": "PCG-PrX"
            }
        ],
    """
    if isinstance(data, list):
        data = data[0]

    if isinstance(data, dict):
        return data[key]

    return data


def get_gaap_period_int(filing_category: dict, year: int) -> int:
    index: int = 0

    index_period: int = int(filing_category[index]["period"]["endDate"][:4])
    while index_period != year:
        index += 1
        index_period = int(filing_category[index]["period"]["endDate"][:4])

    return int(get_value(filing_category[index]))


def get_balance_sheet(filing: dict, index: int) -> BalanceSheet:
    cash: int = 0
    assets: int = 0
    liabilities: int = 0
    equity: int = 0
    for key in filing["BalanceSheets"].keys():
        if "Cash" in key:
            cash += get_gaap_period_int(filing["BalanceSheets"][key], index)
        elif "Assets" in key:
            assets += get_gaap_period_int(filing["BalanceSheets"][key], index)
        elif "Liabilities" in key:
            liabilities += get_gaap_period_int(filing["BalanceSheets"][key], index)
        elif "Equity" in key or "Treasury" in key:
            equity += get_gaap_period_int(filing["BalanceSheets"][key], index)

    assert cash != 0, "Cash not found"
    assert assets != 0, "Assets not found"
    assert liabilities != 0, "Liabilities not found"
    assert equity != 0, "Equity not found"

    return Assets(
        Cash=cash,
        Assets=assets,
        Liabilities=liabilities,
        Equity=equity,
    )


"""
def get_financials(filing: dict, index: int) -> Financials:
    financials: Financials = Financials()
    for key in filing["Financials"].keys():
        if "Revenue" in key:
            financials.Revenue[key] = get_gaap_period_int(
                filing["Financials"][key], index
            )
            financials.Revenue["net"] += financials.Revenue[key]
        elif "Costs" in key:
            financials.Costs[key] = -abs(
                get_gaap_period_int(filing["Financials"][key], index)
            )
            financials.Costs["net"] += financials.Costs[key]
"""

def get_income(filing: dict, index: int) -> Income:
    income: Income = Income()
    for key in filing["StatementsOfIncome"].keys():
        if "Loss" in key:
            pass
        elif "CostOf" in key:
            income.Costs[key] = -abs(
                get_gaap_period_int(filing["StatementsOfIncome"][key], index)
            )
            income.Costs["net"] += income.Costs[key]
        elif "Revenue" in key:
            income.Revenue[key] = get_gaap_period_int(
                filing["StatementsOfIncome"][key], index
            )
            income.Revenue["net"] += income.Revenue[key]
        elif "Administrative" in key:
            income.Operations[key] = -abs(
                get_gaap_period_int(filing["StatementsOfIncome"][key], index)
            )
            income.Operations["net"] += income.Operations[key]
        elif "Interest" in key and "Expense" in key:
            income.Debt[key] = -abs(
                get_gaap_period_int(filing["StatementsOfIncome"][key], index)
            )
            income.Debt["net"] += income.Debt[key]
        elif "Tax" in key:
            income.Taxes[key] = -abs(
                get_gaap_period_int(filing["StatementsOfIncome"][key], index)
            )
            income.Taxes["net"] += income.Taxes[key]
        elif any(term in key for term in income.Expenses["keywords"]):
            income.Expenses[key] = -abs(
                get_gaap_period_int(filing["StatementsOfIncome"][key], index)
            )
            if "Income" in key:
                income.Expenses["net"] -= income.Expenses[key]
            else:
                income.Expenses["net"] += income.Expenses[key]
        elif "Investment" in key:
            income.Investments[key] = abs(
                get_gaap_period_int(filing["StatementsOfIncome"][key], index)
            )
            income.Investments["net"] += income.Investments[key]

    assert income.Costs["net"] <= 0, "Costs can't be positive income"
    assert income.Revenue["net"] > 0, "Revenue can't be negative income"
    assert income.Operations["net"] <= 0, "Operations can't be positive income"
    assert income.Taxes["net"] != 0, "Taxes not found"

    # Check if filing contains the key StatementsOfComprehensiveIncome
    if "StatementsOfComprehensiveIncome" not in filing:
        return income

    for key in filing["StatementsOfComprehensiveIncome"].keys():
        try:
            if "Currency" in key:
                income.CurrencyExchange[key] = get_gaap_period_int(
                    filing["StatementsOfComprehensiveIncome"][key], index
                )
                income.CurrencyExchange["net"] += income.CurrencyExchange[key]
            elif "etirement" in key:
                income.Benefits[key] = get_gaap_period_int(
                    filing["StatementsOfComprehensiveIncome"][key], index
                )
                income.Benefits["net"] += income.Benefits[key]
            elif "lassification" in key:
                income.Reclassification[key] = -abs(
                    get_gaap_period_int(
                        filing["StatementsOfComprehensiveIncome"][key], index
                    )
                )
                income.Reclassification["net"] += income.Reclassification[key]
            elif "IncomeLossTax" in key:
                income.IncomeLossTax[key] = abs(
                    get_gaap_period_int(
                        filing["StatementsOfComprehensiveIncome"][key], index
                    )
                )
                income.IncomeLossTax["net"] += income.IncomeLossTax[key]
        except ValueError as e:
            logger.error(f"Error parsing reclassification: {e}, key: {key}")
            pass

        income.Benefits["net"] = -abs(income.Benefits["net"])

        income.GrossProfit = income.Revenue["net"] + income.Costs["net"]
        income.EBITDA = income.GrossProfit + income.Operations["net"]
        income.NetIncome = (
            income.Revenue["net"]
            + income.Costs["net"]
            + income.Operations["net"]
            + income.Expenses["net"]
            + income.Taxes["net"]
            + income.Debt["net"]
            + income.Investments["net"]
            + income.CurrencyExchange["net"]
            + income.Benefits["net"]
            + income.Reclassification["net"]
            + income.IncomeLossTax["net"]
        )

    return income


def get_finances(filing: dict, index: int) -> Income:
    return get_income(filing, index)
