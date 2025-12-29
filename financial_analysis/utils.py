from models import Keys
from typing import Optional

def get_keys(filing) -> Keys:
    debt_key: str = "" 
    for key in filing["StatementsOfIncome"].keys():
        if "Cost" in key:
            costs_key = key
        elif "Revenue" in key:
            revenue_key = key
        elif "Administrative" in key:
            operations_key = key
        elif "Interest" in key and "Expense" in key:
            debt_key = key
        # elif "Interest" in key and "Income" in key:
        #    interest_income_key = key
        elif "Tax" in key:
            taxes_key = key
        elif "Expense" in key:
            expense_key = key
        
    assert costs_key, "Costs not found" 
    assert revenue_key, "Revenue not found" 
    assert operations_key, "Operations not found" 
    assert taxes_key, "Taxes not found" 
    assert expense_key, "Expenses not found" 

    comprehensive_key = next((k for k in filing["StatementsOfComprehensiveIncome"].keys() if "ComprehensiveIncomeNetOfTax" in k), "")
    assert comprehensive_key, "Comprehensive Income not found" 

    # Update to also look for NetCash in k and write it as a key if found
    cash_flow_key: Optional[str] = None 
    cash_flow_key = next((k for k in filing["StatementsOfCashFlows"].keys() if "NetCash" in k), "")
    if not cash_flow_key:
        cash_flow_key = next((k for k in filing["StatementsOfCashFlows"].keys() if "NetIncome" in k), "")

    assert cash_flow_key, "Cash Flow not found" 

    equity_key:str = ""
    for key in filing["BalanceSheets"].keys():
        if "Cash" in key:
            cash_key = key
        elif "Assets" in key:
            assets_key = key
        elif "Liabilities" in key:
            liabilities_key = key
        elif "Equity" in key:
            equity_key = key

    assert cash_key, "Cash not found" 
    assert assets_key, "Assets not found" 
    assert liabilities_key, "Liabilities not found" 

    if equity_key == "":
        equity_key = next((k for k in filing["BalanceSheets"].keys() if "Treasury" in k), "")

    assert equity_key, "Equity not found" 

    return Keys(
        revenue=revenue_key,
        costs=costs_key,
        operations=operations_key,
        debt=debt_key,
        taxes=taxes_key,
        expenses=expense_key,
        comprehensive_income=comprehensive_key,
        cash_flow=cash_flow_key,
        cash=cash_key,
        assets=assets_key,
        liabilities=liabilities_key,
        equity=equity_key,
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
    return data["value"] if isinstance(data, dict) else (data[0] if isinstance(data, list) else data)
