from financial_analysis.models import Keys
from financial_analysis.models import Finances
import logging

logger = logging.getLogger(__name__)


def gaap_int(key: str, filing_category: dict, index: int) -> int:
    return int(get_value(filing_category[key][index]))


def sum_category(keys: list[str], filing_category: dict, index: int) -> int:
    return sum(int(gaap_int(key, filing_category, index)) for key in keys)


def get_keys(filing: dict) -> Keys:
    debt_keys: list[str] = []
    costs_keys: list[str] = []
    revenue_keys: list[str] = []
    operations_keys: list[str] = []
    taxes_keys: list[str] = []
    expense_keys: list[str] = []
    for key in filing["StatementsOfIncome"].keys():
        if "Loss" in key:
            pass
        elif "Cost" in key:
            costs_keys.append(key)
        elif "Revenue" in key:
            revenue_keys.append(key)
        elif "Administrative" in key:
            operations_keys.append(key)
        elif "Interest" in key and "Expense" in key:
            debt_keys.append(key)
        # elif "Interest" in key and "Income" in key:
        #    interest_income_key = key
        elif "Tax" in key:
            taxes_keys.append(key)
        elif "Expense" in key:
            expense_keys.append(key)

    assert len(costs_keys) > 0, "Costs not found"
    assert len(revenue_keys) > 0, "Revenue not found"
    assert len(operations_keys) > 0, "Operations not found"
    assert len(taxes_keys) > 0, "Taxes not found"
    assert len(expense_keys) > 0, "Expenses not found"

    currency_keys: list[str] = []
    retirement_keys: list[str] = []
    classification_keys: list[str] = []
    income_loss_tax_keys: list[str] = []
    comprehensive_keys: list[str] = []
    for key in filing["StatementsOfComprehensiveIncome"].keys():
        if "Currency" in key:
            currency_keys.append(key)
        elif "etirement" in key:
            retirement_keys.append(key)
        elif "lassification" in key:
            classification_keys.append(key)
        elif "IncomeLossTax" in key:
            income_loss_tax_keys.append(key)
        elif "ComprehensiveIncomeNetOfTax" in key:
            comprehensive_keys.append(key)

    assert len(comprehensive_keys) > 0, "Comprehensive Income not found"

    # Update to also look for NetCash in k and write it as a key if found
    cash_flow_keys = [
        k for k in filing["StatementsOfCashFlows"].keys() if "NetCash" in k
    ]
    if len(cash_flow_keys) == 0:
        cash_flow_keys = [
            k for k in filing["StatementsOfCashFlows"].keys() if "NetIncome" in k
        ]

    assert len(cash_flow_keys) > 0, "Cash Flow not found"

    cash_keys: list[str] = []
    assets_keys: list[str] = []
    liabilities_keys: list[str] = []
    equity_keys: list[str] = []
    for key in filing["BalanceSheets"].keys():
        if "Cash" in key:
            cash_keys.append(key)
        elif "Assets" in key:
            assets_keys.append(key)
        elif "Liabilities" in key:
            liabilities_keys.append(key)
        elif "Equity" in key:
            equity_keys.append(key)

    assert len(cash_keys) > 0, "Cash not found"
    assert len(assets_keys) > 0, "Assets not found"
    assert len(liabilities_keys) > 0, "Liabilities not found"

    if len(equity_keys) == 0:
        equity_keys = [k for k in filing["BalanceSheets"].keys() if "Treasury" in k]

    assert len(equity_keys) > 0, "Equity not found"

    return Keys(
        revenue=revenue_keys,
        costs=costs_keys,
        operations=operations_keys,
        debt=debt_keys,
        taxes=taxes_keys,
        expenses=expense_keys,
        comprehensive_income=comprehensive_keys,
        cash_flow=cash_flow_keys,
        cash=cash_keys,
        assets=assets_keys,
        liabilities=liabilities_keys,
        equity=equity_keys,
    )


def get_finances(filing: dict, index: int) -> Finances:
    debt: int = 0
    costs: int = 0
    revenue: int = 0
    operations: int = 0
    taxes: int = 0
    expenses: int = 0
    investments: int = 0
    for key in filing["StatementsOfIncome"].keys():
        if "Loss" in key:
            pass
        elif "Cost" in key:
            costs -= int(get_value(filing["StatementsOfIncome"][key][index]))
        elif "Revenue" in key:
            revenue += int(get_value(filing["StatementsOfIncome"][key][index]))
        elif "Administrative" in key:
            operations -= int(get_value(filing["StatementsOfIncome"][key][index]))
        elif "Interest" in key and "Expense" in key:
            debt -= int(get_value(filing["StatementsOfIncome"][key][index]))
        elif "Tax" in key:
            taxes -= int(get_value(filing["StatementsOfIncome"][key][index]))
        elif "Expense" in key or "Depreciat" in key or "Restructur" in key:
            expenses -= int(get_value(filing["StatementsOfIncome"][key][index]))
        elif "Investment" in key:
            investments += int(get_value(filing["StatementsOfIncome"][key][index]))

    assert costs < 0, "Costs not found"
    assert revenue > 0, "Revenue not found"
    assert operations < 0, "Operations not found"
    assert taxes != 0, "Taxes not found"

    currency_exchange: int = 0
    benefits: int = 0
    reclassification: int = 0
    income_loss_tax: int = 0
    for key in filing["StatementsOfComprehensiveIncome"].keys():
        try:
            if "Currency" in key:
                currency_exchange += int(
                    get_value(filing["StatementsOfComprehensiveIncome"][key][index])
                )
            elif "etirement" in key:
                benefits += int(
                    get_value(filing["StatementsOfComprehensiveIncome"][key][index])
                )
            elif "lassification" in key:
                reclassification -= int(
                    get_value(filing["StatementsOfComprehensiveIncome"][key][index])
                )

            elif "IncomeLossTax" in key:
                income_loss_tax -= int(
                    get_value(filing["StatementsOfComprehensiveIncome"][key][index])
                )
        except ValueError as e:
            logger.error(f"Error parsing reclassification: {e}, key: {key}")
            pass

        benefits = -abs(benefits)
    """
    # Update to also look for NetCash in k and write it as a key if found
    cash_flow: int = 0
    cash_flow += sum(
        int(get_value(filing["StatementsOfCashFlows"][key][index]))
        for key in filing["StatementsOfCashFlows"].keys()
        if "NetCash" in key
    )

    cash_flow += sum(
        int(get_value(filing["StatementsOfCashFlows"][key][index]))
        for key in filing["StatementsOfCashFlows"].keys()
        if "NetIncome" in key
    )

    assert cash_flow != 0, "Cash Flow not found"

    
    cash_keys: list[str] = []
    assets_keys: list[str] = []
    liabilities_keys: list[str] = []
    equity_keys: list[str] = []
    for key in filing["BalanceSheets"].keys():
        if "Cash" in key:
            cash_keys.append(key)
        elif "Assets" in key:
            assets_keys.append(key)
        elif "Liabilities" in key:
            liabilities_keys.append(key)
        elif "Equity" in key:
            equity_keys.append(key)

    assert len(cash_keys) > 0, "Cash not found"
    assert len(assets_keys) > 0, "Assets not found"
    assert len(liabilities_keys) > 0, "Liabilities not found"

    if len(equity_keys) == 0:
        equity_keys = [k for k in filing["BalanceSheets"].keys() if "Treasury" in k]

    assert len(equity_keys) > 0, "Equity not found"
    """

    return Finances(
        Revenue=revenue,
        Costs=costs,
        GrossProfit=revenue + costs,
        Operations=operations,
        EBITDA=revenue + costs + operations,
        Expenses=expenses,
        Investments=investments,
        Debt=debt,
        Taxes=taxes,
        CurrencyExchange=currency_exchange,
        Benefits=benefits,
        Reclassification=reclassification,
        IncomeLossTax=income_loss_tax,
        NetIncome=revenue
        + costs
        + operations
        + expenses
        + taxes
        + debt
        + investments
        + currency_exchange
        + benefits
        + reclassification
        + income_loss_tax,
    )


"""
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


def get_value(data) -> str:
    """Helper to safely extract values from dict, list, or string."""
    return (
        data["value"]
        if isinstance(data, dict)
        else (data[0] if isinstance(data, list) else data)
    )
