# Financial Analysis

This is a simple financial analysis tool that uses the SEC's EDGAR API to retrieve financial data for a given company.

## Quickstart (MacOS/Linux)

No API key needed — all data comes straight from SEC EDGAR.

```bash
# Choose a company by stock symbol
./Quickstart aapl
```

## TODO

[ ] Add comprehensive expenses.

[ ] Double check period with year argument

## Resources

Now totally independent: filings are located via the [EDGAR submissions API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) and parsed from each filing's raw XBRL (instance + presentation linkbase). Originally bootstrapped with [sec-api](https://github.com/janlukasschroeder/sec-api-python); a [Rust](https://github.com/TiesdeKok/fast_xbrl_parser/tree/master) port is in progress.

o [XBLR Guide](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)
