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